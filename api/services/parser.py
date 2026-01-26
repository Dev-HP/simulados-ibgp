import re
import logging
from typing import Dict, List, Any
import PyPDF2
import io

logger = logging.getLogger(__name__)

class SyllabusParser:
    """
    Parser hierárquico de editais.
    Extrai: disciplina > tópico > subtópico
    Preserva referência à fonte (arquivo, página/linha)
    """
    
    def __init__(self):
        self.disciplinas_conhecidas = [
            "Hardware", "Algoritmos", "Lógica de Programação",
            "Banco de Dados", "Sistemas Operacionais", "Redes",
            "Segurança", "Informática", "Excel", "Legislação",
            "LGPD", "Marco Civil", "Linux", "Windows"
        ]
    
    def extract_from_pdf(self, pdf_content: bytes) -> str:
        """Extrai texto de PDF"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                # Adicionar referência de página
                text += f"\n[PÁGINA {page_num}]\n{page_text}"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            raise
    
    def parse_hierarchical(self, content: str) -> Dict[str, Any]:
        """
        Parse hierárquico do conteúdo.
        Retorna estrutura: {disciplinas: [{nome, topicos: [{nome, subtopico, reference}]}]}
        """
        lines = content.split('\n')
        structure = {
            'disciplinas': [],
            'metadata': {
                'total_lines': len(lines),
                'source': 'edital'
            }
        }
        
        current_disciplina = None
        current_topico = None
        line_num = 0
        
        for line in lines:
            line_num += 1
            line = line.strip()
            
            if not line:
                continue
            
            # Detectar página
            page_match = re.match(r'\[PÁGINA (\d+)\]', line)
            if page_match:
                current_page = page_match.group(1)
                continue
            
            # Detectar disciplina (maiúsculas ou padrões conhecidos)
            if self._is_disciplina(line):
                current_disciplina = {
                    'nome': line,
                    'topicos': [],
                    'reference': f'linha {line_num}'
                }
                structure['disciplinas'].append(current_disciplina)
                continue
            
            # Detectar tópico (numeração ou bullet points)
            if self._is_topico(line):
                if current_disciplina is None:
                    # Criar disciplina genérica
                    current_disciplina = {
                        'nome': 'Geral',
                        'topicos': [],
                        'reference': f'linha {line_num}'
                    }
                    structure['disciplinas'].append(current_disciplina)
                
                current_topico = {
                    'nome': self._clean_topico(line),
                    'subtopicos': [],
                    'reference': f'linha {line_num}'
                }
                current_disciplina['topicos'].append(current_topico)
                continue
            
            # Detectar subtópico
            if current_topico and self._is_subtopico(line):
                subtopico = {
                    'nome': self._clean_topico(line),
                    'reference': f'linha {line_num}'
                }
                current_topico['subtopicos'].append(subtopico)
        
        return structure
    
    def _is_disciplina(self, line: str) -> bool:
        """Detecta se linha é uma disciplina"""
        # Maiúsculas
        if line.isupper() and len(line) > 3:
            return True
        
        # Palavras conhecidas
        for disc in self.disciplinas_conhecidas:
            if disc.lower() in line.lower():
                return True
        
        return False
    
    def _is_topico(self, line: str) -> bool:
        """Detecta se linha é um tópico"""
        # Numeração: 1., 1.1, a), etc
        if re.match(r'^[\d\.]+\s+', line) or re.match(r'^[a-z]\)', line):
            return True
        
        # Bullet points
        if line.startswith('-') or line.startswith('•'):
            return True
        
        return False
    
    def _is_subtopico(self, line: str) -> bool:
        """Detecta se linha é um subtópico"""
        # Sub-numeração: 1.1.1, a.1, etc
        if re.match(r'^[\d\.]{3,}\s+', line):
            return True
        
        # Indentação
        if line.startswith('  ') or line.startswith('\t'):
            return True
        
        return False
    
    def _clean_topico(self, line: str) -> str:
        """Remove numeração e símbolos do tópico"""
        # Remove numeração
        line = re.sub(r'^[\d\.]+\s+', '', line)
        line = re.sub(r'^[a-z]\)\s+', '', line)
        line = re.sub(r'^[-•]\s+', '', line)
        
        return line.strip()
