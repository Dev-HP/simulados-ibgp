import logging
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import PyPDF2
import io

from models import Question, Topic, DifficultyLevel, QAStatus
from services.qa_validator import QAValidator

logger = logging.getLogger(__name__)

class QuestionImporter:
    """
    Importador de questões de provas reais.
    Suporta PDF e TXT com questões formatadas.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.validator = QAValidator()
    
    def import_from_pdf(
        self,
        pdf_content: bytes,
        source_name: str,
        disciplina: str = "Informática"
    ) -> List[Question]:
        """Importa questões de um PDF de prova"""
        
        try:
            # Extrair texto do PDF
            text = self._extract_text_from_pdf(pdf_content)
            
            # Parsear questões
            questions_data = self._parse_questions_from_text(text, source_name, disciplina)
            
            # Salvar no banco
            saved_questions = []
            for q_data in questions_data:
                question = self._save_question(q_data)
                if question:
                    saved_questions.append(question)
            
            logger.info(f"Imported {len(saved_questions)} questions from {source_name}")
            return saved_questions
            
        except Exception as e:
            logger.error(f"Error importing from PDF: {str(e)}")
            return []
    
    def import_from_text(
        self,
        text_content: str,
        source_name: str,
        disciplina: str = "Informática"
    ) -> List[Question]:
        """Importa questões de texto formatado"""
        
        questions_data = self._parse_questions_from_text(text_content, source_name, disciplina)
        
        saved_questions = []
        for q_data in questions_data:
            question = self._save_question(q_data)
            if question:
                saved_questions.append(question)
        
        logger.info(f"Imported {len(saved_questions)} questions from {source_name}")
        return saved_questions
    
    def _extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extrai texto de PDF"""
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    
    def _parse_questions_from_text(
        self,
        text: str,
        source_name: str,
        disciplina: str
    ) -> List[Dict[str, Any]]:
        """
        Parseia questões do texto.
        Suporta formatos comuns de provas:
        
        QUESTÃO 1
        Enunciado...
        A) alternativa
        B) alternativa
        C) alternativa
        D) alternativa
        Gabarito: A
        """
        questions = []
        
        # Padrão para detectar questões
        # Aceita: "QUESTÃO 1", "Questão 01", "1.", "01)"
        question_pattern = r'(?:QUESTÃO|Questão|QUESTAO|Questao)\s*(\d+)|^(\d+)[\.\)]'
        
        # Dividir texto em blocos de questões
        lines = text.split('\n')
        current_question = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            
            # Detectar início de nova questão
            if re.match(question_pattern, line, re.IGNORECASE):
                # Salvar questão anterior
                if current_question and current_text:
                    question_data = self._parse_question_block('\n'.join(current_text), source_name, disciplina)
                    if question_data:
                        questions.append(question_data)
                
                # Iniciar nova questão
                current_question = line
                current_text = []
            else:
                current_text.append(line)
        
        # Salvar última questão
        if current_question and current_text:
            question_data = self._parse_question_block('\n'.join(current_text), source_name, disciplina)
            if question_data:
                questions.append(question_data)
        
        return questions
    
    def _parse_question_block(
        self,
        block: str,
        source_name: str,
        disciplina: str
    ) -> Optional[Dict[str, Any]]:
        """Parseia um bloco de questão individual"""
        
        try:
            question_data = {
                'disciplina': disciplina,
                'referencia': source_name,
                'qa_status': QAStatus.APPROVED
            }
            
            # Extrair enunciado (tudo antes da primeira alternativa)
            alt_pattern = r'^[A-D][\)\.]'
            lines = block.split('\n')
            enunciado_lines = []
            alternativas_start = -1
            
            for i, line in enumerate(lines):
                if re.match(alt_pattern, line.strip()):
                    alternativas_start = i
                    break
                enunciado_lines.append(line)
            
            if alternativas_start == -1:
                return None
            
            question_data['enunciado'] = ' '.join(enunciado_lines).strip()
            
            # Extrair alternativas
            alternativas = {'A': '', 'B': '', 'C': '', 'D': ''}
            current_letter = None
            
            for line in lines[alternativas_start:]:
                line = line.strip()
                
                # Detectar letra da alternativa
                match = re.match(r'^([A-D])[\)\.](.+)', line)
                if match:
                    current_letter = match.group(1)
                    alternativas[current_letter] = match.group(2).strip()
                elif current_letter and line and not line.startswith('Gabarito'):
                    # Continuar alternativa anterior
                    alternativas[current_letter] += ' ' + line
            
            # Adicionar alternativas
            for letter in ['A', 'B', 'C', 'D']:
                if alternativas[letter]:
                    question_data[f'alternativa_{letter.lower()}'] = alternativas[letter].strip()
            
            # Extrair gabarito
            gabarito_match = re.search(r'Gabarito:\s*([A-D])', block, re.IGNORECASE)
            if gabarito_match:
                question_data['gabarito'] = gabarito_match.group(1).upper()
            else:
                # Se não encontrar gabarito explícito, tentar detectar
                # (algumas provas marcam com asterisco ou negrito)
                question_data['gabarito'] = 'A'  # Default
            
            # Extrair explicação (se houver)
            explicacao_match = re.search(r'(?:Explicação|Justificativa|Comentário):\s*(.+)', block, re.IGNORECASE | re.DOTALL)
            if explicacao_match:
                question_data['explicacao_detalhada'] = explicacao_match.group(1).strip()
            else:
                question_data['explicacao_detalhada'] = f"A alternativa {question_data['gabarito']} está correta."
            
            # Detectar tópico do enunciado
            question_data['topico'] = self._detect_topic(question_data['enunciado'])
            
            # Estimar dificuldade
            question_data['dificuldade'] = self._estimate_difficulty(question_data['enunciado'])
            
            # Estimar tempo
            question_data['estimativa_tempo'] = self._estimate_time(question_data['dificuldade'])
            
            # Validar campos obrigatórios
            required = ['enunciado', 'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d', 'gabarito']
            if all(field in question_data for field in required):
                return question_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing question block: {str(e)}")
            return None
    
    def _detect_topic(self, enunciado: str) -> str:
        """Detecta tópico baseado em palavras-chave"""
        
        topics_keywords = {
            'Hardware': ['hardware', 'processador', 'memória', 'ram', 'disco', 'cpu', 'placa'],
            'Redes': ['rede', 'tcp', 'ip', 'protocolo', 'internet', 'lan', 'wan', 'ethernet'],
            'Linux': ['linux', 'unix', 'shell', 'bash', 'comando'],
            'Windows': ['windows', 'cmd', 'powershell', 'registro'],
            'Banco de Dados': ['banco', 'sql', 'select', 'database', 'tabela', 'query'],
            'Segurança': ['segurança', 'criptografia', 'firewall', 'vírus', 'malware'],
            'Programação': ['algoritmo', 'programação', 'código', 'função', 'variável']
        }
        
        enunciado_lower = enunciado.lower()
        
        for topic, keywords in topics_keywords.items():
            if any(keyword in enunciado_lower for keyword in keywords):
                return topic
        
        return 'Geral'
    
    def _estimate_difficulty(self, enunciado: str) -> DifficultyLevel:
        """Estima dificuldade baseado no enunciado"""
        
        # Indicadores de dificuldade
        hard_indicators = ['exceto', 'incorreto', 'não', 'falso', 'analise', 'compare']
        easy_indicators = ['é', 'são', 'define', 'significa']
        
        enunciado_lower = enunciado.lower()
        
        if any(ind in enunciado_lower for ind in hard_indicators):
            return DifficultyLevel.DIFICIL
        elif any(ind in enunciado_lower for ind in easy_indicators):
            return DifficultyLevel.FACIL
        else:
            return DifficultyLevel.MEDIO
    
    def _estimate_time(self, dificuldade: DifficultyLevel) -> int:
        """Estima tempo baseado na dificuldade"""
        if dificuldade == DifficultyLevel.FACIL:
            return 2
        elif dificuldade == DifficultyLevel.MEDIO:
            return 3
        else:
            return 5
    
    def _save_question(self, question_data: Dict[str, Any]) -> Optional[Question]:
        """Valida e salva questão no banco"""
        
        try:
            # Validação QA
            qa_result = self.validator.validate(question_data)
            question_data['qa_score'] = qa_result['score']
            
            # Salvar mesmo se não passar na validação (questões reais)
            # mas marcar o status
            if qa_result['status'] == QAStatus.REJECTED:
                question_data['qa_status'] = QAStatus.REVIEW_REQUIRED
            
            # Verificar duplicatas
            existing = self.db.query(Question).filter(
                Question.enunciado == question_data['enunciado']
            ).first()
            
            if existing:
                logger.warning(f"Duplicate question found, skipping")
                return None
            
            # Salvar
            question = Question(**question_data)
            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            
            return question
            
        except Exception as e:
            logger.error(f"Error saving question: {str(e)}")
            self.db.rollback()
            return None
