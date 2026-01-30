#!/usr/bin/env python3
"""
Verificar quantas questões existem no banco
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Adicionar o diretório api ao path
api_dir = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_dir)

from database import SessionLocal
from models import Question, Topic

def verificar_banco():
    db = SessionLocal()
    
    print("🔍 VERIFICANDO BANCO DE DADOS")
    print("="*50)
    
    # Contar questões por disciplina
    disciplinas = ["Informática", "Português", "Matemática", "Raciocínio Lógico", "Legislação", "Conhecimentos Gerais"]
    
    total_questoes = 0
    
    for disciplina in disciplinas:
        count = db.query(Question).filter(Question.disciplina == disciplina).count()
        total_questoes += count
        print(f"📚 {disciplina:25s}: {count:4d} questões")
    
    print("="*50)
    print(f"🎯 TOTAL: {total_questoes} questões")
    
    # Contar tópicos
    total_topicos = db.query(Topic).count()
    print(f"📖 TÓPICOS: {total_topicos} tópicos")
    
    # Verificar se há questões recentes
    questoes_recentes = db.query(Question).order_by(Question.created_at.desc()).limit(5).all()
    
    if questoes_recentes:
        print(f"\n📝 ÚLTIMAS 5 QUESTÕES:")
        for q in questoes_recentes:
            print(f"  • {q.disciplina} - {q.topico} ({q.created_at.strftime('%d/%m %H:%M')})")
    else:
        print(f"\n⚠️  Nenhuma questão encontrada")
    
    db.close()

if __name__ == "__main__":
    verificar_banco()