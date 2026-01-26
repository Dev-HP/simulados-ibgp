from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import engine, get_db, Base
from routers import syllabus, questions, simulados, users, analytics, export
from models import User
from auth import get_current_user

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Simulados IBGP",
    description="API para simulados adaptativos - Técnico em Informática",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(syllabus.router, prefix="/api", tags=["Syllabus"])
app.include_router(questions.router, prefix="/api", tags=["Questions"])
app.include_router(simulados.router, prefix="/api", tags=["Simulados"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(export.router, prefix="/api", tags=["Export"])

@app.get("/")
async def root():
    return {
        "message": "Sistema de Simulados IBGP - API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
