"""
Router para estatísticas e informações do Gemini
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import google.generativeai as genai

from database import get_db
from auth import get_current_user
from models import User

router = APIRouter()

@router.get("/stats")
async def get_gemini_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna estatísticas do Gemini"""
    try:
        # Verificar se API key está configurada
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        
        # Configurar Gemini
        genai.configure(api_key=api_key)
        
        # Informações básicas (simuladas para tier gratuito)
        return {
            "status": "configured",
            "tier": "free",
            "api_key_configured": True,
            "requests_today": 0,  # Em produção, isso viria de um cache/banco
            "daily_limit": 1400,
            "restante": 1400,
            "models_available": [
                "gemini-2.5-flash-lite",
                "gemini-2.5-flash", 
                "gemini-2.0-flash"
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "tier": "unknown",
            "api_key_configured": False,
            "error": str(e)
        }