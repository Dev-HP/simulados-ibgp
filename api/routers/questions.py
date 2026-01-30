from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
import os

from database import get_db
from models import Question, Topic
from schemas import QuestionResponse, QuestionCreate, GenerateBankRequest
from services.question_generator import QuestionGenerator
from services.hybrid_ai_generator import HybridAIGenerator
from services.question_importer import QuestionImporter

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-bank")
async def generate_question_bank(
    request: GenerateBankRequest,
    db: Session = Depends(get_db)
):
    """
    Gera banco de questões baseado nos tópicos do edital.
    Mínimo 30 questões por tópico amplo, 10 para tópicos pequenos.
    """
    try:
        generator = QuestionGenerator(db)
        
        # Buscar tópicos
        topics = db.query(Topic).all()
        if not topics:
            raise HTTPException(status_code=400, detail="No topics found. Upload syllabus first.")
        
        # Gerar questões
        generated_count = generator.generate_for_topics(
            topics=topics,
            min_questions=request.min_questions_per_topic,
            seeds=request.seeds
        )
        
        return {
            "message": "Question bank generated successfully",
            "total_questions": generated_count,
            "topics_covered": len(topics)
        }
        
    except Exception as e:
        logger.error(f"Error generating question bank: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions", response_model=List[QuestionResponse])
async def list_questions(
    disciplina: Optional[str] = None,
    topico: Optional[str] = None,
    dificuldade: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    
    if disciplina:
        query = query.filter(Question.disciplina == disciplina)
    if topico:
        query = query.filter(Question.topico == topico)
    if dificuldade:
        query = query.filter(Question.dificuldade == dificuldade)
    
    questions = query.offset(skip).limit(limit).all()
    return questions

@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/questions", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """Criar questão manualmente"""
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.post("/import-questions")
async def import_questions(
    file: UploadFile = File(...),
    disciplina: str = "Informática",
    db: Session = Depends(get_db)
):
    """
    Importa questões de provas reais (PDF ou TXT).
    
    Formato esperado:
    QUESTÃO 1
    Enunciado...
    A) alternativa
    B) alternativa
    C) alternativa
    D) alternativa
    Gabarito: A
    """
    try:
        importer = QuestionImporter(db)
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            questions = importer.import_from_pdf(content, file.filename, disciplina)
        else:
            text = content.decode('utf-8')
            questions = importer.import_from_text(text, file.filename, disciplina)
        
        return {
            "message": "Questions imported successfully",
            "total_imported": len(questions),
            "source": file.filename
        }
        
    except Exception as e:
        logger.error(f"Error importing questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-with-ai")
async def generate_with_ai(
    topic_id: int,
    quantity: int = 10,
    difficulty: Optional[str] = None,
    use_references: bool = True,
    strategy: str = "huggingface_only",
    db: Session = Depends(get_db)
):
    """
    Gera questões usando HuggingFace-only.
    
    Parâmetros:
    - topic_id: ID do tópico
    - quantity: Quantidade de questões a gerar
    - difficulty: FACIL, MEDIO ou DIFICIL (opcional)
    - use_references: Usar questões reais como referência
    - strategy: Sempre "huggingface_only" (outros valores são ignorados)
    """
    try:
        # Verificar se HuggingFace API key está configurada
        has_huggingface = bool(os.getenv('HUGGINGFACE_API_KEY'))
        
        if not has_huggingface:
            raise HTTPException(
                status_code=400,
                detail="HUGGINGFACE_API_KEY não configurada. Configure no arquivo .env"
            )
        
        # Buscar tópico
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        # Buscar questões de referência
        reference_questions = []
        if use_references:
            refs = db.query(Question).filter(
                Question.disciplina == topic.disciplina
            ).limit(5).all()
            reference_questions = [
                {
                    'enunciado': q.enunciado,
                    'alternativa_a': q.alternativa_a,
                    'alternativa_b': q.alternativa_b,
                    'alternativa_c': q.alternativa_c,
                    'alternativa_d': q.alternativa_d,
                    'gabarito': q.gabarito,
                    'explicacao_detalhada': q.explicacao_detalhada
                }
                for q in refs
            ]
        
        # Gerar com HuggingFace-only
        generator = HybridAIGenerator(db)
        questions = generator.generate_questions_with_ai(
            topic=topic,
            quantity=quantity,
            reference_questions=reference_questions,
            difficulty=difficulty,
            strategy="huggingface_only"  # Sempre HuggingFace
        )
        
        # Status dos geradores
        status = generator.get_status()
        
        return {
            "message": "Questions generated with HuggingFace successfully",
            "total_generated": len(questions),
            "topic": topic.topico,
            "references_used": len(reference_questions),
            "strategy_used": "huggingface_only",
            "generators_status": {
                "gemini_available": False,  # Sempre False
                "huggingface_available": status["huggingface_available"],
                "success_rates": status["success_rates"],
                "mode": "huggingface_only"
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating with AI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/improve-question/{question_id}")
async def improve_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Melhora uma questão existente usando HuggingFace.
    """
    try:
        if not os.getenv('HUGGINGFACE_API_KEY'):
            raise HTTPException(
                status_code=400,
                detail="HUGGINGFACE_API_KEY não configurada"
            )
        
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Usar HybridAIGenerator para melhorar a questão
        generator = HybridAIGenerator(db)
        
        # Buscar tópico da questão
        topic = db.query(Topic).filter(
            Topic.disciplina == question.disciplina,
            Topic.topico == question.topico
        ).first()
        
        if not topic:
            # Criar tópico se não existir
            topic = Topic(
                disciplina=question.disciplina,
                topico=question.topico,
                subtopico=question.subtopico
            )
            db.add(topic)
            db.commit()
            db.refresh(topic)
        
        # Gerar uma versão melhorada da questão
        improved_questions = generator.generate_questions_with_ai(
            topic=topic,
            quantity=1,
            reference_questions=[{
                'enunciado': question.enunciado,
                'alternativa_a': question.alternativa_a,
                'alternativa_b': question.alternativa_b,
                'alternativa_c': question.alternativa_c,
                'alternativa_d': question.alternativa_d,
                'gabarito': question.gabarito,
                'explicacao_detalhada': question.explicacao_detalhada
            }],
            difficulty=question.dificuldade.value if question.dificuldade else "MEDIO",
            strategy="huggingface_only"
        )
        
        if improved_questions:
            return {
                "message": "Question improved with HuggingFace successfully",
                "question_id": question_id,
                "improved_count": len(improved_questions)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to improve question")
            
    except Exception as e:
        logger.error(f"Error improving question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-generators-status")
async def get_ai_generators_status(db: Session = Depends(get_db)):
    """
    Retorna status do gerador HuggingFace-only.
    """
    try:
        generator = HybridAIGenerator(db)
        status = generator.get_status()
        test_results = generator.test_all_generators()
        
        return {
            "status": "ok",
            "mode": "huggingface_only",
            "generators": {
                "gemini": {
                    "available": False,
                    "api_key_configured": False,
                    "test_result": {"status": "disabled", "message": "Gemini disabled by configuration"},
                    "success_rate": 0.0
                },
                "huggingface": {
                    "available": status["huggingface_available"],
                    "api_key_configured": bool(os.getenv('HUGGINGFACE_API_KEY')),
                    "test_result": test_results.get("huggingface", {}),
                    "success_rate": status["success_rates"]["huggingface"]
                }
            },
            "stats": status["stats"],
            "recommendations": {
                "best_for_informatica": "huggingface_only",
                "best_for_portuguese": "huggingface_only",
                "most_reliable": "huggingface"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting AI generators status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gemini-stats")
async def get_gemini_stats():
    """
    Retorna estatísticas de uso da API Gemini.
    Mostra limites do free tier e uso atual.
    """
    from services.rate_limiter import gemini_rate_limiter
    
    stats = gemini_rate_limiter.get_stats()
    
    return {
        "status": "ok",
        "tier": "free",
        "limits": {
            "per_minute": stats['limit_per_minute'],
            "per_day": stats['limit_per_day']
        },
        "usage": {
            "last_minute": stats['requests_last_minute'],
            "today": stats['requests_today'],
            "total": stats['total_requests'],
            "blocked": stats['blocked_requests']
        },
        "remaining": {
            "minute": stats['remaining_minute'],
            "day": stats['remaining_day']
        },
        "percentage": {
            "minute": round(stats['usage_percentage_minute'], 2),
            "day": round(stats['usage_percentage_day'], 2)
        },
        "warnings": [
            "⚠️ Limite por minuto atingido" if stats['remaining_minute'] < 5 else None,
            "⚠️ Limite diário próximo" if stats['remaining_day'] < 100 else None
        ]
    }

@router.post("/generate-complete-exam")
async def generate_complete_exam(db: Session = Depends(get_db)):
    """
    Gera TODAS as 60 questões da prova real do concurso.
    Segue EXATAMENTE a distribuição do edital IBGP.
    
    Distribuição:
    - Informática: 30 questões (50%)
    - Português: 9 questões (15%)
    - Matemática: 6 questões (10%)
    - Raciocínio Lógico: 4 questões (7%)
    - Legislação: 7 questões (11%)
    - Conhecimentos Gerais: 4 questões (7%)
    
    Tempo estimado: 15-20 minutos
    """
    try:
        # Verificar se HuggingFace API key está configurada
        has_huggingface = bool(os.getenv('HUGGINGFACE_API_KEY'))
        
        if not has_huggingface:
            raise HTTPException(
                status_code=400,
                detail="HUGGINGFACE_API_KEY não configurada. Configure no arquivo .env"
            )
        
        # Distribuição exata do edital
        DISTRIBUICAO_EDITAL = {
            "Informática": {
                "total": 30,
                "topicos": {
                    "Hardware - Componentes internos": 4,
                    "Hardware - Periféricos": 2,
                    "Redes - Conceitos básicos": 3,
                    "Redes - TCP/IP": 3,
                    "Redes - Equipamentos": 2,
                    "Windows 10/11": 4,
                    "Linux básico": 2,
                    "Word": 2,
                    "Excel": 3,
                    "PowerPoint": 1,
                    "Segurança da Informação": 2,
                    "Internet e E-mail": 2
                }
            },
            "Português": {
                "total": 9,
                "topicos": {
                    "Interpretação de Texto": 3,
                    "Concordância": 2,
                    "Regência": 1,
                    "Crase": 1,
                    "Ortografia": 1,
                    "Pontuação": 1
                }
            },
            "Matemática": {
                "total": 6,
                "topicos": {
                    "Operações básicas": 2,
                    "Porcentagem": 2,
                    "Regra de Três": 1,
                    "Frações": 1
                }
            },
            "Raciocínio Lógico": {
                "total": 4,
                "topicos": {
                    "Sequências": 2,
                    "Proposições": 2
                }
            },
            "Legislação": {
                "total": 7,
                "topicos": {
                    "Estatuto dos Servidores RO": 3,
                    "Ética no Serviço Público": 2,
                    "Lei de Licitações": 2
                }
            },
            "Conhecimentos Gerais": {
                "total": 4,
                "topicos": {
                    "Rondônia": 2,
                    "Porto Velho": 1,
                    "Atualidades": 1
                }
            }
        }
        
        generator = HybridAIGenerator(db)
        total_geradas = 0
        relatorio = {}
        
        # Gerar questões por disciplina e tópico
        for disciplina, config in DISTRIBUICAO_EDITAL.items():
            logger.info(f"Gerando questões para {disciplina}...")
            relatorio[disciplina] = {}
            
            for topico, quantidade in config['topicos'].items():
                try:
                    # Buscar ou criar tópico
                    topic = db.query(Topic).filter(
                        Topic.disciplina == disciplina,
                        Topic.topico == topico
                    ).first()
                    
                    if not topic:
                        topic = Topic(disciplina=disciplina, topico=topico)
                        db.add(topic)
                        db.commit()
                        db.refresh(topic)
                    
                    # Buscar questões de referência
                    reference_questions = []
                    refs = db.query(Question).filter(
                        Question.disciplina == disciplina
                    ).limit(3).all()
                    
                    if refs:
                        reference_questions = [
                            {
                                'enunciado': q.enunciado,
                                'alternativa_a': q.alternativa_a,
                                'alternativa_b': q.alternativa_b,
                                'alternativa_c': q.alternativa_c,
                                'alternativa_d': q.alternativa_d,
                                'gabarito': q.gabarito,
                                'explicacao_detalhada': q.explicacao_detalhada
                            }
                            for q in refs
                        ]
                    
                    # Gerar questões usando HuggingFace-only
                    questions = generator.generate_questions_with_ai(
                        topic=topic,
                        quantity=quantidade,
                        reference_questions=reference_questions,
                        difficulty="MEDIO",
                        strategy="huggingface_only"  # Usar apenas HuggingFace
                    )
                    
                    geradas = len(questions)
                    total_geradas += geradas
                    relatorio[disciplina][topico] = geradas
                    
                    logger.info(f"  {topico}: {geradas}/{quantidade} questões")
                    
                    # Aguardar para respeitar rate limit do HuggingFace
                    import time
                    time.sleep(2)  # Menor delay para HuggingFace
                    
                except Exception as e:
                    logger.error(f"Erro ao gerar {topico}: {str(e)}")
                    relatorio[disciplina][topico] = 0
        
        return {
            "message": "Prova completa gerada com HuggingFace successfully!",
            "total_generated": total_geradas,
            "expected": 60,
            "percentage": round((total_geradas/60)*100, 1),
            "strategy_used": "huggingface_only",
            "report": relatorio
        }
        
    except Exception as e:
        logger.error(f"Error generating complete exam: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
