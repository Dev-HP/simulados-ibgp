"""
Router para geração de provas completas
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import logging

from database import get_db
from models import Topic, Question
from auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

# Templates de provas completas - IBGP Porto Velho/RO
TEMPLATES_PROVAS = {
    "tecnico_informatica_completo": {
        "nome": "Técnico em Informática - IBGP (Prova Completa)",
        "total_questoes": 60,
        "distribuicao": {
            "Informática": 30,
            "Português": 10,
            "Matemática": 8,
            "Raciocínio Lógico": 7,
            "Legislação": 5
        },
        "descricao": "Prova completa para concurso de Técnico em Informática"
    },
    "tecnico_informatica_padrao": {
        "nome": "Técnico em Informática - IBGP (Padrão)",
        "total_questoes": 50,
        "distribuicao": {
            "Informática": 25,
            "Português": 10,
            "Matemática": 8,
            "Raciocínio Lógico": 5,
            "Legislação": 2
        },
        "descricao": "Prova padrão com foco em Informática"
    },
    "conhecimentos_basicos": {
        "nome": "Conhecimentos Básicos",
        "total_questoes": 40,
        "distribuicao": {
            "Português": 15,
            "Matemática": 12,
            "Raciocínio Lógico": 8,
            "Conhecimentos Gerais": 5
        },
        "descricao": "Prova de conhecimentos básicos (sem Informática)"
    },
    "informatica_especifica": {
        "nome": "Informática - Conhecimentos Específicos",
        "total_questoes": 40,
        "distribuicao": {
            "Informática": 40
        },
        "descricao": "Prova focada apenas em Informática"
    },
    "portugues_especifico": {
        "nome": "Português - Específico",
        "total_questoes": 30,
        "distribuicao": {
            "Português": 30
        },
        "descricao": "Prova focada apenas em Português"
    },
    "matematica_raciocinio": {
        "nome": "Matemática e Raciocínio Lógico",
        "total_questoes": 30,
        "distribuicao": {
            "Matemática": 15,
            "Raciocínio Lógico": 15
        },
        "descricao": "Prova de exatas e lógica"
    },
    "legislacao_especifica": {
        "nome": "Legislação - Específico",
        "total_questoes": 20,
        "distribuicao": {
            "Legislação": 20
        },
        "descricao": "Prova focada em Legislação (RO e Federal)"
    },
    "conhecimentos_gerais_especifico": {
        "nome": "Conhecimentos Gerais - RO",
        "total_questoes": 20,
        "distribuicao": {
            "Conhecimentos Gerais": 20
        },
        "descricao": "Prova sobre Rondônia e Porto Velho"
    }
}

@router.get("/templates-provas")
async def listar_templates():
    """Lista templates de provas disponíveis para Técnico em Informática - IBGP"""
    return {
        "templates": [
            {
                "id": key,
                "nome": value["nome"],
                "total_questoes": value["total_questoes"],
                "disciplinas": list(value["distribuicao"].keys()),
                "descricao": value["descricao"]
            }
            for key, value in TEMPLATES_PROVAS.items()
        ]
    }

@router.post("/gerar-prova-completa")
async def gerar_prova_completa(
    template_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Gera uma prova completa baseada em um template
    """
    if template_id not in TEMPLATES_PROVAS:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    template = TEMPLATES_PROVAS[template_id]
    questoes_selecionadas = []
    estatisticas = {}
    
    try:
        # Para cada disciplina no template
        for disciplina, quantidade in template["distribuicao"].items():
            # Buscar questões da disciplina
            questoes = db.query(Question).filter(
                Question.disciplina == disciplina
            ).limit(quantidade * 2).all()  # Buscar o dobro para ter margem
            
            # Selecionar aleatoriamente
            import random
            questoes_disponiveis = min(len(questoes), quantidade)
            selecionadas = random.sample(questoes, questoes_disponiveis)
            
            questoes_selecionadas.extend(selecionadas)
            estatisticas[disciplina] = {
                "solicitadas": quantidade,
                "encontradas": questoes_disponiveis
            }
        
        # Embaralhar questões
        import random
        random.shuffle(questoes_selecionadas)
        
        return {
            "template": template["nome"],
            "total_questoes": len(questoes_selecionadas),
            "questoes": [
                {
                    "id": q.id,
                    "disciplina": q.disciplina,
                    "topico": q.topico,
                    "enunciado": q.enunciado,
                    "alternativa_a": q.alternativa_a,
                    "alternativa_b": q.alternativa_b,
                    "alternativa_c": q.alternativa_c,
                    "alternativa_d": q.alternativa_d,
                    "dificuldade": q.dificuldade.value if q.dificuldade else "MEDIO"
                }
                for q in questoes_selecionadas
            ],
            "estatisticas": estatisticas,
            "aviso": "Algumas disciplinas podem ter menos questões que o solicitado" if len(questoes_selecionadas) < template["total_questoes"] else None
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar prova completa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/estatisticas-banco")
async def estatisticas_banco(db: Session = Depends(get_db)):
    """Retorna estatísticas do banco de questões por disciplina"""
    
    disciplinas = db.query(Question.disciplina).distinct().all()
    estatisticas = {}
    
    for (disciplina,) in disciplinas:
        count = db.query(Question).filter(Question.disciplina == disciplina).count()
        estatisticas[disciplina] = count
    
    return {
        "total_questoes": db.query(Question).count(),
        "por_disciplina": estatisticas,
        "disciplinas_disponiveis": list(estatisticas.keys())
    }
