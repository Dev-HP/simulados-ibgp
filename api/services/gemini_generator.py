import logging
import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Question, Topic, DifficultyLevel, QAStatus
from services.qa_validator import QAValidator
from services.rate_limiter import gemini_rate_limiter

logger = logging.getLogger(__name__)

class GeminiQuestionGenerator:
    """
    Gerador de questões usando Gemini Pro.
    Gera questões realistas baseadas em exemplos de provas reais.
    """
    
    def __init__(self, db: Session, api_key: Optional[str] = None):
        self.db = db
        self.validator = QAValidator()
        
        # Configurar Gemini
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        genai.configure(api_key=api_key)
        # Tentar modelos em ordem de prioridade (fallback automático)
        self.models = [
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash-lite',
            'gemini-flash-lite-latest'
        ]
        self.current_model = None
        self._initialize_working_model()
    
    def _initialize_working_model(self):
        """Encontra um modelo que funciona"""
        for model_name in self.models:
            try:
                model = genai.GenerativeModel(model_name)
                # Teste rápido
                response = model.generate_content("OK")
                if response.text:
                    self.model = model
                    self.current_model = model_name
                    logger.info(f"Using Gemini model: {model_name}")
                    return
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {str(e)[:100]}")
                continue
        
        raise ValueError("Nenhum modelo Gemini disponível. Verifique API key e quota.")
    
    def _generate_with_retry(self, prompt: str, max_retries: int = 3):
        """Gera conteúdo com retry automático e fallback de modelos"""
        last_error = None
        
        for attempt in range(max_retries):
            for model_name in self.models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        if model_name != self.current_model:
                            logger.info(f"Switched to model: {model_name}")
                            self.current_model = model_name
                            self.model = model
                        return response
                        
                except Exception as e:
                    last_error = e
                    error_msg = str(e).lower()
                    
                    if "quota" in error_msg or "429" in error_msg:
                        logger.warning(f"Quota exceeded for {model_name}, trying next model...")
                        continue
                    elif "expired" in error_msg or "invalid" in error_msg:
                        logger.error(f"API key issue with {model_name}: {e}")
                        continue
                    else:
                        logger.error(f"Unexpected error with {model_name}: {e}")
                        continue
            
            # Se chegou aqui, todos os modelos falharam nesta tentativa
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10  # Backoff exponencial
                logger.warning(f"All models failed, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
        
        # Todas as tentativas falharam
        raise Exception(f"Failed to generate content after {max_retries} attempts. Last error: {last_error}")
    
    def generate_questions_with_ai(
        self,
        topic: Topic,
        quantity: int = 10,
        reference_questions: List[Dict] = None,
        difficulty: Optional[DifficultyLevel] = None
    ) -> List[Question]:
        """
        Gera questões usando Gemini Pro baseadas em exemplos reais.
        """
        generated = []
        
        # Criar prompt com exemplos
        prompt = self._build_prompt(topic, quantity, reference_questions, difficulty)
        
        try:
            # Verificar rate limit
            can_make, error_msg = gemini_rate_limiter.can_make_request()
            if not can_make:
                logger.error(f"Rate limit exceeded: {error_msg}")
                raise HTTPException(status_code=429, detail=error_msg)
            
            # Gerar com Gemini (com retry automático)
            response = self._generate_with_retry(prompt)
            
            # Registrar requisição
            gemini_rate_limiter.record_request()
            
            # Parsear resposta
            questions_data = self._parse_gemini_response(response.text, topic)
            
            # Validar e salvar
            for q_data in questions_data:
                question = self._validate_and_save(q_data)
                if question:
                    generated.append(question)
            
            logger.info(f"Generated {len(generated)} questions with Gemini for topic {topic.id}")
            
        except Exception as e:
            logger.error(f"Error generating with Gemini: {str(e)}")
        
        return generated
    
    def _build_prompt(
        self,
        topic: Topic,
        quantity: int,
        reference_questions: List[Dict],
        difficulty: Optional[DifficultyLevel]
    ) -> str:
        """Constrói prompt otimizado para o Gemini com contexto do concurso"""
        
        # Contexto específico por disciplina
        contexto_disciplina = {
            "Informática": """
CONTEXTO: Concurso para Técnico em Informática da Câmara Municipal de Porto Velho/RO.
FOCO: Conhecimentos práticos e aplicados ao dia a dia de um técnico em órgão público.
ESTILO: Questões objetivas, diretas, sem pegadinhas excessivas.
EXEMPLOS DE TEMAS: Hardware (manutenção, componentes), Redes (TCP/IP, cabeamento), 
Sistemas Operacionais (Windows 10/11, Linux), Segurança (backup, antivírus), 
Office (Word, Excel, PowerPoint), Internet e E-mail.
""",
            "Português": """
CONTEXTO: Língua Portuguesa para concurso público de nível médio/técnico.
FOCO: Interpretação de texto, gramática aplicada, redação oficial.
ESTILO: Textos curtos e objetivos, questões práticas sobre uso correto da língua.
EXEMPLOS: Concordância verbal/nominal, regência, crase, pontuação, ortografia.
""",
            "Matemática": """
CONTEXTO: Matemática básica para concurso de nível médio/técnico.
FOCO: Problemas práticos do cotidiano, cálculos aplicados.
ESTILO: Questões diretas com situações reais.
EXEMPLOS: Porcentagem, regra de três, frações, equações simples, geometria básica.
""",
            "Raciocínio Lógico": """
CONTEXTO: Raciocínio lógico para concurso público.
FOCO: Sequências, proposições, problemas lógicos, diagramas.
ESTILO: Questões que exigem interpretação e dedução lógica.
""",
            "Legislação": """
CONTEXTO: Legislação aplicada ao serviço público, com foco em Rondônia e Porto Velho.
FOCO: Constituição Federal, Lei 8.112/90, Estatuto dos Servidores de RO, 
Ética no Serviço Público, Lei de Licitações (14.133/2021), Lei de Acesso à Informação.
ESTILO: Questões sobre direitos, deveres, procedimentos administrativos.
IMPORTANTE: Quando aplicável, mencionar especificidades de Rondônia.
""",
            "Conhecimentos Gerais": """
CONTEXTO: Conhecimentos gerais com foco em Rondônia e Porto Velho.
FOCO: Geografia de RO (rios, municípios, economia), História de Porto Velho 
(fundação, desenvolvimento), Atualidades do Brasil e região Norte.
ESTILO: Questões sobre fatos relevantes, dados geográficos, história local.
IMPORTANTE: Priorizar informações sobre Rondônia e Porto Velho.
"""
        }
        
        contexto = contexto_disciplina.get(topic.disciplina, "")
        
        nivel_dificuldade = {
            DifficultyLevel.FACIL: "FÁCIL - Conceitos básicos, diretos, sem pegadinhas",
            DifficultyLevel.MEDIO: "MÉDIO - Requer conhecimento intermediário e interpretação",
            DifficultyLevel.DIFICIL: "DIFÍCIL - Conhecimento avançado, análise crítica"
        }
        
        nivel = nivel_dificuldade.get(difficulty, "VARIADO - Mix de fácil, médio e difícil")
        
        prompt = f"""Você é um especialista em elaborar questões de concurso público brasileiro, 
especificamente para o cargo de TÉCNICO EM INFORMÁTICA da CÂMARA MUNICIPAL DE PORTO VELHO/RO.

{contexto}

═══════════════════════════════════════════════════════════════════

TAREFA: Gerar {quantity} questões de múltipla escolha sobre:
📚 DISCIPLINA: {topic.disciplina}
📖 TÓPICO: {topic.topico}
{f'📌 SUBTÓPICO: {topic.subtopico}' if topic.subtopico else ''}

NÍVEL DE DIFICULDADE: {nivel}

═══════════════════════════════════════════════════════════════════

REGRAS OBRIGATÓRIAS:

1. ENUNCIADO:
   ✓ Claro, objetivo e sem ambiguidades
   ✓ Contexto realista (situação de trabalho, caso prático)
   ✓ Tamanho: 2-4 linhas (máximo 300 caracteres)
   ✓ Evitar "assinale a alternativa correta" (já está implícito)

2. ALTERNATIVAS:
   ✓ Exatamente 4 opções (A, B, C, D)
   ✓ Apenas 1 alternativa TOTALMENTE correta
   ✓ Distratores plausíveis (erros comuns, conceitos relacionados)
   ✓ Tamanho similar entre alternativas
   ✓ Evitar "todas as anteriores" ou "nenhuma das anteriores"
   ✓ Não usar "a e b estão corretas" (escolha única!)

3. GABARITO:
   ✓ Apenas uma letra: A, B, C ou D
   ✓ Distribuir gabaritos de forma equilibrada

4. EXPLICAÇÃO:
   ✓ Por que a resposta está correta (2-3 linhas)
   ✓ Por que as outras estão erradas (1 linha cada)
   ✓ Referência técnica quando aplicável

5. ESTILO:
   ✓ Linguagem formal mas acessível
   ✓ Termos técnicos corretos
   ✓ Sem pegadinhas excessivas
   ✓ Foco no conhecimento prático

═══════════════════════════════════════════════════════════════════
"""
        
        # Adicionar exemplos de questões reais
        if reference_questions and len(reference_questions) > 0:
            prompt += "\n📋 EXEMPLOS DE QUESTÕES REAIS (use como referência de estilo):\n\n"
            for i, ref in enumerate(reference_questions[:2], 1):
                prompt += f"═══ EXEMPLO {i} ═══\n"
                prompt += f"📝 {ref.get('enunciado', '')}\n\n"
                prompt += f"A) {ref.get('alternativa_a', '')}\n"
                prompt += f"B) {ref.get('alternativa_b', '')}\n"
                prompt += f"C) {ref.get('alternativa_c', '')}\n"
                prompt += f"D) {ref.get('alternativa_d', '')}\n\n"
                prompt += f"✅ GABARITO: {ref.get('gabarito', '')}\n"
                prompt += f"💡 {ref.get('explicacao_detalhada', '')}\n\n"
        
        # Dicas específicas por tópico
        dicas_topico = {
            "Hardware": "Foque em componentes reais (CPU, RAM, HD, SSD), manutenção preventiva, identificação de problemas.",
            "Redes": "Aborde protocolos (TCP/IP, HTTP, FTP), endereçamento IP, equipamentos (switch, roteador), cabeamento.",
            "Windows": "Versões 10/11, gerenciamento de arquivos, configurações, ferramentas administrativas.",
            "Linux": "Comandos básicos (ls, cd, chmod, chown), permissões, estrutura de diretórios.",
            "Segurança da Informação": "Backup, antivírus, firewall, políticas de senha, criptografia básica.",
            "Microsoft Office": "Word (formatação, tabelas), Excel (fórmulas, funções), PowerPoint (apresentações).",
            "Português": "Interpretação de texto, concordância, regência, crase, pontuação.",
            "Matemática": "Problemas práticos, porcentagem, regra de três, frações.",
            "Legislação": "Quando for sobre Rondônia, mencione especificidades locais.",
            "Rondônia": "Capital Porto Velho, rios (Madeira, Guaporé), economia (agropecuária, mineração).",
            "Porto Velho": "Fundação (1914), Estrada de Ferro Madeira-Mamoré, Rio Madeira, usinas hidrelétricas."
        }
        
        dica = next((v for k, v in dicas_topico.items() if k.lower() in topic.topico.lower()), "")
        if dica:
            prompt += f"\n💡 DICA PARA ESTE TÓPICO: {dica}\n\n"
        
        prompt += """
═══════════════════════════════════════════════════════════════════

📤 FORMATO DE SAÍDA (OBRIGATÓRIO - copie exatamente):

---QUESTAO---
ENUNCIADO: [texto do enunciado sem "assinale a alternativa correta"]
A) [alternativa A]
B) [alternativa B]
C) [alternativa C]
D) [alternativa D]
GABARITO: [apenas a letra: A, B, C ou D]
EXPLICACAO: [explicação detalhada: por que a correta está certa e as outras erradas]
DIFICULDADE: [FACIL, MEDIO ou DIFICIL]
TEMPO_ESTIMADO: [número de 1 a 6 minutos]
---FIM---

═══════════════════════════════════════════════════════════════════

🚀 GERE AS {quantity} QUESTÕES AGORA (uma por vez, seguindo o formato acima):
"""
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str, topic: Topic) -> List[Dict[str, Any]]:
        """Parseia resposta do Gemini em formato estruturado"""
        questions = []
        
        # Dividir por questões
        parts = response_text.split('---QUESTAO---')
        
        for part in parts:
            if '---FIM---' not in part:
                continue
            
            try:
                # Extrair campos
                question_data = {
                    'topic_id': topic.id,
                    'disciplina': topic.disciplina,
                    'topico': topic.topico,
                    'subtopico': topic.subtopico,
                    'referencia': topic.reference,
                    'keywords': [topic.disciplina, topic.topico],
                    'qa_status': QAStatus.APPROVED
                }
                
                # Enunciado
                if 'ENUNCIADO:' in part:
                    enunciado = part.split('ENUNCIADO:')[1].split('A)')[0].strip()
                    question_data['enunciado'] = enunciado
                
                # Alternativas
                for letter in ['A', 'B', 'C', 'D']:
                    next_letter = chr(ord(letter) + 1) if letter != 'D' else 'GABARITO'
                    if f'{letter})' in part:
                        alt_text = part.split(f'{letter})')[1].split(f'{next_letter}')[0].strip()
                        question_data[f'alternativa_{letter.lower()}'] = alt_text
                
                # Gabarito
                if 'GABARITO:' in part:
                    gabarito = part.split('GABARITO:')[1].split('\n')[0].strip()
                    question_data['gabarito'] = gabarito.upper()
                
                # Explicação
                if 'EXPLICACAO:' in part:
                    explicacao = part.split('EXPLICACAO:')[1].split('DIFICULDADE:')[0].strip()
                    question_data['explicacao_detalhada'] = explicacao
                
                # Dificuldade
                if 'DIFICULDADE:' in part:
                    dif_text = part.split('DIFICULDADE:')[1].split('\n')[0].strip().upper()
                    if 'FACIL' in dif_text:
                        question_data['dificuldade'] = DifficultyLevel.FACIL
                    elif 'DIFICIL' in dif_text:
                        question_data['dificuldade'] = DifficultyLevel.DIFICIL
                    else:
                        question_data['dificuldade'] = DifficultyLevel.MEDIO
                
                # Tempo estimado
                if 'TEMPO_ESTIMADO:' in part:
                    tempo_text = part.split('TEMPO_ESTIMADO:')[1].split('\n')[0].strip()
                    try:
                        question_data['estimativa_tempo'] = int(''.join(filter(str.isdigit, tempo_text)))
                    except:
                        question_data['estimativa_tempo'] = 3
                
                # Validar campos obrigatórios
                required = ['enunciado', 'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d', 'gabarito']
                if all(field in question_data for field in required):
                    questions.append(question_data)
                
            except Exception as e:
                logger.error(f"Error parsing question: {str(e)}")
                continue
        
        return questions
    
    def _validate_and_save(self, question_data: Dict[str, Any]) -> Optional[Question]:
        """Valida e salva questão no banco"""
        try:
            # Validação QA
            qa_result = self.validator.validate(question_data)
            question_data['qa_score'] = qa_result['score']
            question_data['qa_status'] = qa_result['status']
            
            # Só salvar se aprovada
            if qa_result['status'] == QAStatus.REJECTED:
                logger.warning(f"Question rejected by QA: {qa_result['issues']}")
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
    
    def generate_contextual_question(
        self,
        topic: Topic,
        context_type: str = "trabalho"
    ) -> Optional[Question]:
        """
        Gera questão com contexto específico (trabalho na Câmara, situação real de Porto Velho, etc.)
        
        Args:
            topic: Tópico da questão
            context_type: Tipo de contexto ("trabalho", "porto_velho", "rondonia", "pratico")
        """
        
        contextos = {
            "trabalho": f"""
Crie uma questão sobre {topic.topico} ({topic.disciplina}) ambientada em uma situação 
REAL de trabalho na Câmara Municipal de Porto Velho.

EXEMPLO DE CONTEXTO:
"João, técnico em informática da Câmara Municipal de Porto Velho, precisa..."
"Durante a manutenção dos computadores do setor administrativo..."
"O servidor responsável pela rede da Câmara identificou..."

A questão deve ser PRÁTICA e relacionada ao dia a dia do cargo.
""",
            "porto_velho": f"""
Crie uma questão sobre {topic.topico} ({topic.disciplina}) que mencione ou se relacione 
com PORTO VELHO, capital de Rondônia.

ELEMENTOS PARA INCLUIR (quando aplicável):
- Câmara Municipal de Porto Velho
- Rio Madeira
- Estrada de Ferro Madeira-Mamoré
- Usinas hidrelétricas (Santo Antônio, Jirau)
- População aproximada: 500 mil habitantes
- Fundação: 1914

A questão deve ser técnica mas com contexto local.
""",
            "rondonia": f"""
Crie uma questão sobre {topic.topico} ({topic.disciplina}) relacionada ao estado de RONDÔNIA.

ELEMENTOS PARA INCLUIR (quando aplicável):
- Órgãos públicos de Rondônia
- Legislação estadual
- Características da região Norte
- Contexto amazônico

A questão deve ter relevância para o concurso público estadual/municipal.
""",
            "pratico": f"""
Crie uma questão EXTREMAMENTE PRÁTICA sobre {topic.topico} ({topic.disciplina}).

FOCO: Situação real que um técnico em informática enfrenta no dia a dia.
EXEMPLOS: Resolver problema de hardware, configurar rede, instalar software, 
fazer backup, dar suporte a usuários, etc.

A questão deve testar conhecimento aplicado, não apenas teoria.
"""
        }
        
        contexto_escolhido = contextos.get(context_type, contextos["pratico"])
        
        prompt = f"""Você é especialista em questões de concurso para Técnico em Informática.

{contexto_escolhido}

REGRAS:
1. Enunciado com contexto realista (2-4 linhas)
2. 4 alternativas (A, B, C, D) - apenas 1 correta
3. Distratores plausíveis
4. Explicação detalhada

FORMATO DE SAÍDA:
---QUESTAO---
ENUNCIADO: [texto com contexto]
A) [alternativa A]
B) [alternativa B]
C) [alternativa C]
D) [alternativa D]
GABARITO: [A, B, C ou D]
EXPLICACAO: [explicação detalhada]
DIFICULDADE: [FACIL, MEDIO ou DIFICIL]
TEMPO_ESTIMADO: [1-6 minutos]
---FIM---

Gere a questão agora:
"""
        
        try:
            # Verificar rate limit
            can_make, error_msg = gemini_rate_limiter.can_make_request()
            if not can_make:
                logger.error(f"Rate limit exceeded: {error_msg}")
                return None
            
            response = self.model.generate_content(prompt)
            gemini_rate_limiter.record_request()
            
            questions_data = self._parse_gemini_response(response.text, topic)
            
            if questions_data:
                return self._validate_and_save(questions_data[0])
                
        except Exception as e:
            logger.error(f"Error generating contextual question: {str(e)}")
        
        return None
    
    def improve_existing_question(self, question: Question) -> Optional[Question]:
        """Melhora uma questão existente usando Gemini"""
        
        prompt = f"""Você é um especialista em questões de concurso. Melhore a seguinte questão:

QUESTÃO ATUAL:
Enunciado: {question.enunciado}
A) {question.alternativa_a}
B) {question.alternativa_b}
C) {question.alternativa_c}
D) {question.alternativa_d}
Gabarito: {question.gabarito}

MELHORIAS NECESSÁRIAS:
1. Tornar o enunciado mais claro e objetivo
2. Melhorar os distratores (alternativas erradas mais plausíveis)
3. Adicionar contexto técnico realista
4. Garantir que apenas uma alternativa está correta

Retorne a questão melhorada no mesmo formato.
"""
        
        try:
            # Verificar rate limit
            can_make, error_msg = gemini_rate_limiter.can_make_request()
            if not can_make:
                logger.error(f"Rate limit exceeded: {error_msg}")
                raise HTTPException(status_code=429, detail=error_msg)
            
            response = self.model.generate_content(prompt)
            
            # Registrar requisição
            gemini_rate_limiter.record_request()
            
            improved_data = self._parse_gemini_response(response.text, question.topic)
            
            if improved_data:
                # Atualizar questão existente
                for key, value in improved_data[0].items():
                    if hasattr(question, key):
                        setattr(question, key, value)
                
                self.db.commit()
                return question
                
        except Exception as e:
            logger.error(f"Error improving question: {str(e)}")
        
        return None
