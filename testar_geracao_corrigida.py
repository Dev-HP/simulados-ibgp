#!/usr/bin/env python3
"""
Teste da versão corrigida do gerador Gemini
"""
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

sys.path.append('api')

from sqlalchemy.orm import Session
from database import get_db, engine
from models import Topic, Base
from services.gemini_generator_fixed import GeminiQuestionGeneratorFixed

def testar_geracao():
    print("🧪 TESTANDO GERADOR GEMINI CORRIGIDO")
    print("=" * 50)
    
    # Criar tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    # Obter sessão do banco
    db = next(get_db())
    
    try:
        # Buscar um tópico para testar
        topic = db.query(Topic).filter(Topic.disciplina == "Informática").first()
        
        if not topic:
            print("❌ Nenhum tópico encontrado")
            return
        
        print(f"📚 Testando tópico: {topic.topico}")
        print(f"🎯 Disciplina: {topic.disciplina}")
        
        # Inicializar gerador corrigido
        generator = GeminiQuestionGeneratorFixed(db)
        
        # Gerar 1 questão de teste
        print("\n🔄 Gerando questão...")
        questions = generator.generate_questions_with_ai(
            topic=topic,
            quantity=1
        )
        
        if questions:
            q = questions[0]
            print(f"\n✅ QUESTÃO GERADA COM SUCESSO!")
            print(f"📝 Enunciado: {q.enunciado[:100]}...")
            print(f"🅰️ A) {q.alternativa_a[:50]}...")
            print(f"🅱️ B) {q.alternativa_b[:50]}...")
            print(f"🅲️ C) {q.alternativa_c[:50]}...")
            print(f"🅳️ D) {q.alternativa_d[:50]}...")
            print(f"✅ Gabarito: {q.gabarito}")
            print(f"💡 Explicação: {q.explicacao_detalhada[:100]}...")
        else:
            print("❌ Nenhuma questão foi gerada")
    
    except Exception as e:
        print(f"💥 Erro: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    testar_geracao()