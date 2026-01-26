import csv
import json
import logging
from typing import List
from io import StringIO

from models import Question

logger = logging.getLogger(__name__)

class ExportService:
    """
    Serviço de export de questões em múltiplos formatos.
    Suporta: GIFT, CSV, JSON
    """
    
    def export_gift(self, questions: List[Question]) -> str:
        """
        Export para formato GIFT (Moodle).
        """
        gift_content = []
        
        for q in questions:
            # Título
            gift_content.append(f"// {q.disciplina} - {q.topico}")
            gift_content.append(f"::{q.id}:: {q.enunciado} {{")
            
            # Alternativas
            for letter in ['A', 'B', 'C', 'D']:
                alt = getattr(q, f'alternativa_{letter.lower()}')
                prefix = "=" if letter == q.gabarito else "~"
                gift_content.append(f"  {prefix}{alt}")
            
            gift_content.append("}")
            
            # Feedback
            gift_content.append(f"#### {q.explicacao_detalhada}")
            gift_content.append("")
        
        return "\n".join(gift_content)
    
    def export_csv(self, questions: List[Question]) -> str:
        """
        Export para formato CSV.
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'ID', 'Disciplina', 'Tópico', 'Subtópico', 'Enunciado',
            'Alternativa A', 'Alternativa B', 'Alternativa C', 'Alternativa D',
            'Gabarito', 'Explicação', 'Referência', 'Dificuldade',
            'Tempo Estimado', 'Keywords'
        ])
        
        # Dados
        for q in questions:
            writer.writerow([
                q.id,
                q.disciplina,
                q.topico,
                q.subtopico or '',
                q.enunciado,
                q.alternativa_a,
                q.alternativa_b,
                q.alternativa_c,
                q.alternativa_d,
                q.gabarito,
                q.explicacao_detalhada,
                q.referencia or '',
                q.dificuldade.value,
                q.estimativa_tempo or '',
                ','.join(q.keywords) if q.keywords else ''
            ])
        
        return output.getvalue()
    
    def export_json(self, questions: List[Question]) -> str:
        """
        Export para formato JSON.
        """
        data = []
        
        for q in questions:
            data.append({
                'id': q.id,
                'disciplina': q.disciplina,
                'topico': q.topico,
                'subtopico': q.subtopico,
                'enunciado': q.enunciado,
                'alternativas': {
                    'A': q.alternativa_a,
                    'B': q.alternativa_b,
                    'C': q.alternativa_c,
                    'D': q.alternativa_d
                },
                'gabarito': q.gabarito,
                'explicacao': q.explicacao_detalhada,
                'referencia': q.referencia,
                'dificuldade': q.dificuldade.value,
                'estimativa_tempo': q.estimativa_tempo,
                'keywords': q.keywords,
                'qa_score': q.qa_score,
                'qa_status': q.qa_status.value
            })
        
        return json.dumps(data, ensure_ascii=False, indent=2)
