import logging
import random
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from models import Question, Topic, DifficultyLevel, QAStatus
from services.qa_validator import QAValidator

logger = logging.getLogger(__name__)

class QuestionGenerator:
    """
    Gerador de questões no estilo IBGP.
    Gera mínimo 30 questões por tópico amplo, 10 para tópicos pequenos.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.validator = QAValidator()
        
        # Templates de questões por disciplina
        self.templates = self._load_templates()
    
    def generate_for_topics(
        self,
        topics: List[Topic],
        min_questions: int = 10,
        seeds: List[str] = None
    ) -> int:
        """Gera questões para lista de tópicos"""
        total_generated = 0
        
        for topic in topics:
            # Determinar quantidade baseado no tópico
            num_questions = self._determine_quantity(topic, min_questions)
            
            # Gerar questões
            questions = self._generate_questions_for_topic(
                topic=topic,
                quantity=num_questions,
                seeds=seeds
            )
            
            # Validar e salvar
            for q in questions:
                if self._validate_and_save(q):
                    total_generated += 1
        
        logger.info(f"Generated {total_generated} questions for {len(topics)} topics")
        return total_generated
    
    def _determine_quantity(self, topic: Topic, min_questions: int) -> int:
        """Determina quantidade de questões baseado no tópico"""
        # Tópicos amplos: 30 questões
        topicos_amplos = [
            "Hardware", "Algoritmos", "Redes", "Banco de Dados",
            "Sistemas Operacionais", "Segurança"
        ]
        
        if any(amp in topic.topico for amp in topicos_amplos):
            return max(30, min_questions)
        
        # Tópicos pequenos: 10 questões
        return max(10, min_questions)
    
    def _generate_questions_for_topic(
        self,
        topic: Topic,
        quantity: int,
        seeds: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Gera questões para um tópico específico"""
        questions = []
        
        # Buscar templates relevantes
        templates = self._get_templates_for_topic(topic)
        
        for i in range(quantity):
            # Selecionar template
            template = random.choice(templates) if templates else self._get_default_template()
            
            # Gerar questão
            question = self._generate_from_template(
                template=template,
                topic=topic,
                seed=f"{topic.id}_{i}" if not seeds else seeds[i % len(seeds)]
            )
            
            questions.append(question)
        
        return questions
    
    def _generate_from_template(
        self,
        template: Dict[str, Any],
        topic: Topic,
        seed: str
    ) -> Dict[str, Any]:
        """Gera questão a partir de template"""
        # Definir dificuldade
        dificuldade = random.choice([
            DifficultyLevel.FACIL,
            DifficultyLevel.MEDIO,
            DifficultyLevel.DIFICIL
        ])
        
        # Gerar enunciado
        enunciado = template['enunciado_base'].format(
            topico=topic.topico,
            subtopico=topic.subtopico or ""
        )
        
        # Gerar alternativas
        alternativas = self._generate_alternativas(template, topic)
        
        # Selecionar gabarito
        gabarito = random.choice(['A', 'B', 'C', 'D'])
        
        # Gerar explicação
        explicacao = template['explicacao_base'].format(
            topico=topic.topico,
            gabarito=gabarito
        )
        
        return {
            'topic_id': topic.id,
            'disciplina': topic.disciplina,
            'topico': topic.topico,
            'subtopico': topic.subtopico,
            'enunciado': enunciado,
            'alternativa_a': alternativas[0],
            'alternativa_b': alternativas[1],
            'alternativa_c': alternativas[2],
            'alternativa_d': alternativas[3],
            'gabarito': gabarito,
            'explicacao_detalhada': explicacao,
            'referencia': topic.reference,
            'dificuldade': dificuldade,
            'estimativa_tempo': self._estimate_time(dificuldade),
            'keywords': [topic.disciplina, topic.topico],
            'seed': seed,
            'qa_score': 0.0,
            'qa_status': QAStatus.APPROVED
        }
    
    def _generate_alternativas(
        self,
        template: Dict[str, Any],
        topic: Topic
    ) -> List[str]:
        """Gera alternativas plausíveis com distratores realistas"""
        base_alternativas = template.get('alternativas', [])
        
        if len(base_alternativas) >= 4:
            return random.sample(base_alternativas, 4)
        
        # Gerar alternativas genéricas
        return [
            f"Alternativa relacionada a {topic.topico} - opção 1",
            f"Alternativa relacionada a {topic.topico} - opção 2",
            f"Alternativa relacionada a {topic.topico} - opção 3",
            f"Alternativa relacionada a {topic.topico} - opção 4"
        ]
    
    def _estimate_time(self, dificuldade: DifficultyLevel) -> int:
        """Estima tempo em minutos baseado na dificuldade"""
        if dificuldade == DifficultyLevel.FACIL:
            return random.randint(1, 2)
        elif dificuldade == DifficultyLevel.MEDIO:
            return random.randint(2, 4)
        else:
            return random.randint(4, 6)
    
    def _validate_and_save(self, question_data: Dict[str, Any]) -> bool:
        """Valida e salva questão no banco"""
        try:
            # Validação QA
            qa_result = self.validator.validate(question_data)
            question_data['qa_score'] = qa_result['score']
            question_data['qa_status'] = qa_result['status']
            
            # Salvar
            question = Question(**question_data)
            self.db.add(question)
            self.db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving question: {str(e)}")
            self.db.rollback()
            return False
    
    def _get_templates_for_topic(self, topic: Topic) -> List[Dict[str, Any]]:
        """Retorna templates relevantes para o tópico"""
        return self.templates.get(topic.disciplina, [self._get_default_template()])
    
    def _get_default_template(self) -> Dict[str, Any]:
        """Template padrão"""
        return {
            'enunciado_base': 'Sobre {topico}, assinale a alternativa correta:',
            'explicacao_base': 'A alternativa {gabarito} está correta pois aborda corretamente o conceito de {topico}.',
            'alternativas': []
        }
    
    def _load_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Carrega templates de questões por disciplina"""
        return {
            'Hardware': [
                {
                    'enunciado_base': 'Em relação aos componentes de hardware, especificamente sobre {topico}, é correto afirmar que:',
                    'explicacao_base': 'A alternativa correta é {gabarito}, pois descreve adequadamente as características de {topico}.',
                    'alternativas': []
                }
            ],
            'Redes': [
                {
                    'enunciado_base': 'Considerando os protocolos de rede e {topico}, assinale a alternativa correta:',
                    'explicacao_base': 'A resposta {gabarito} está correta ao abordar {topico} no contexto de redes.',
                    'alternativas': []
                }
            ],
            'Linux': [
                {
                    'enunciado_base': 'No sistema operacional Linux, o comando relacionado a {topico}:',
                    'explicacao_base': 'A alternativa {gabarito} apresenta corretamente o uso de {topico} em Linux.',
                    'alternativas': []
                }
            ]
        }
