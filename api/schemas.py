from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    FACIL = "fácil"
    MEDIO = "médio"
    DIFICIL = "difícil"

class QAStatus(str, Enum):
    APPROVED = "approved"
    REVIEW_REQUIRED = "review_required"
    REJECTED = "rejected"

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Syllabus schemas
class SyllabusUpload(BaseModel):
    filename: str
    content: str

class SyllabusResponse(BaseModel):
    id: int
    filename: str
    parsed_structure: Optional[Dict[str, Any]]
    uploaded_at: datetime
    message: str = "Conteúdo programático recebido"

    class Config:
        from_attributes = True

# Topic schemas
class TopicCreate(BaseModel):
    disciplina: str
    topico: str
    subtopico: Optional[str] = None
    reference: Optional[str] = None

class TopicResponse(BaseModel):
    id: int
    disciplina: str
    topico: str
    subtopico: Optional[str]
    reference: Optional[str]

    class Config:
        from_attributes = True

# Question schemas
class QuestionCreate(BaseModel):
    disciplina: str
    topico: str
    subtopico: Optional[str] = None
    enunciado: str
    alternativa_a: str
    alternativa_b: str
    alternativa_c: str
    alternativa_d: str
    gabarito: str = Field(..., pattern="^[A-D]$")
    explicacao_detalhada: str
    referencia: Optional[str] = None
    dificuldade: DifficultyLevel
    estimativa_tempo: Optional[int] = None
    keywords: Optional[List[str]] = None
    seed: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    disciplina: str
    topico: str
    subtopico: Optional[str]
    enunciado: str
    alternativa_a: str
    alternativa_b: str
    alternativa_c: str
    alternativa_d: str
    gabarito: str
    explicacao_detalhada: str
    referencia: Optional[str]
    dificuldade: DifficultyLevel
    estimativa_tempo: Optional[int]
    keywords: Optional[List[str]]
    qa_score: Optional[float]
    qa_status: QAStatus

    class Config:
        from_attributes = True

# Simulado schemas
class SimuladoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    numero_questoes: int = Field(..., gt=0)
    tempo_total: Optional[int] = None
    disciplinas: Optional[List[str]] = None
    dificuldade_alvo: Optional[str] = None
    pesos: Optional[Dict[str, float]] = None
    aleatorizacao_por_topico: bool = True

class SimuladoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    numero_questoes: int
    tempo_total: Optional[int]
    disciplinas: Optional[List[str]]
    is_oficial: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Answer schemas
class AnswerSubmit(BaseModel):
    question_id: int
    resposta: str = Field(..., pattern="^[A-D]$")
    tempo_resposta: Optional[int] = None

class AnswerFeedback(BaseModel):
    is_correct: bool
    gabarito: str
    explicacao: str
    referencia: Optional[str]
    tipo_erro: Optional[str]
    questoes_similares: List[int]

# Result schemas
class SimuladoResultResponse(BaseModel):
    id: int
    simulado_id: int
    score: float
    tempo_total: Optional[int]
    acertos_por_disciplina: Dict[str, Any]
    tempo_medio_questao: Optional[float]
    indice_confianca: Optional[float]
    plano_estudo: Optional[Dict[str, Any]]
    completed_at: datetime

    class Config:
        from_attributes = True

# Analytics schemas
class UserAnalytics(BaseModel):
    total_simulados: int
    media_score: float
    disciplinas_fortes: List[str]
    disciplinas_fracas: List[str]
    tempo_medio_questao: float
    progresso_temporal: List[Dict[str, Any]]

# Generate bank schemas
class GenerateBankRequest(BaseModel):
    seeds: Optional[List[str]] = None
    min_questions_per_topic: int = 10
    target_topics: Optional[List[str]] = None
