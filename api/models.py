from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class DifficultyLevel(str, enum.Enum):
    FACIL = "fácil"
    MEDIO = "médio"
    DIFICIL = "difícil"

class QAStatus(str, enum.Enum):
    APPROVED = "approved"
    REVIEW_REQUIRED = "review_required"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    results = relationship("SimuladoResult", back_populates="user")
    answers = relationship("UserAnswer", back_populates="user")

class Syllabus(Base):
    __tablename__ = "syllabus"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    parsed_structure = Column(JSON)
    source_reference = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    topics = relationship("Topic", back_populates="syllabus")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabus.id"))
    disciplina = Column(String, nullable=False, index=True)
    topico = Column(String, nullable=False)
    subtopico = Column(String)
    reference = Column(String)
    
    syllabus = relationship("Syllabus", back_populates="topics")
    questions = relationship("Question", back_populates="topic")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    disciplina = Column(String, nullable=False, index=True)
    topico = Column(String, nullable=False)
    subtopico = Column(String)
    enunciado = Column(Text, nullable=False)
    alternativa_a = Column(Text, nullable=False)
    alternativa_b = Column(Text, nullable=False)
    alternativa_c = Column(Text, nullable=False)
    alternativa_d = Column(Text, nullable=False)
    gabarito = Column(String(1), nullable=False)
    explicacao_detalhada = Column(Text, nullable=False)
    referencia = Column(String)
    dificuldade = Column(Enum(DifficultyLevel), nullable=False)
    estimativa_tempo = Column(Integer)
    keywords = Column(JSON)
    seed = Column(String)
    qa_score = Column(Float)
    qa_status = Column(Enum(QAStatus), default=QAStatus.APPROVED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    topic = relationship("Topic", back_populates="questions")
    answers = relationship("UserAnswer", back_populates="question")

class Simulado(Base):
    __tablename__ = "simulados"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text)
    numero_questoes = Column(Integer, nullable=False)
    tempo_total = Column(Integer)
    disciplinas = Column(JSON)
    dificuldade_alvo = Column(String)
    is_oficial = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    results = relationship("SimuladoResult", back_populates="simulado")
    questions = relationship("SimuladoQuestion", back_populates="simulado")

class SimuladoQuestion(Base):
    __tablename__ = "simulado_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    ordem = Column(Integer, nullable=False)
    
    simulado = relationship("Simulado", back_populates="questions")

class SimuladoResult(Base):
    __tablename__ = "simulado_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    simulado_id = Column(Integer, ForeignKey("simulados.id"))
    score = Column(Float, nullable=False)
    tempo_total = Column(Integer)
    acertos_por_disciplina = Column(JSON)
    tempo_medio_questao = Column(Float)
    indice_confianca = Column(Float)
    plano_estudo = Column(JSON)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="results")
    simulado = relationship("Simulado", back_populates="results")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    simulado_result_id = Column(Integer, ForeignKey("simulado_results.id"))
    resposta = Column(String(1), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    tempo_resposta = Column(Integer)
    tipo_erro = Column(String)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
