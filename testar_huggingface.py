#!/usr/bin/env python3
"""
Teste do gerador HuggingFace
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Topic
from services.huggingface_generator import HuggingFaceQuestionGenerator

def testar_huggingface():
    """Testa o gerador HuggingFace"""
    
    print("🤗 TESTANDO HUGGINGFACE GENERATOR")
    print("=" * 50)
    
    # Verificar API key
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        print("❌ HUGGINGFACE_API_KEY não configurada!")
        print("💡 Configure no arquivo .env:")
        print("HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("\n🔗 Obtenha sua chave em: https://huggingface.co/settings/tokens")
        return
    
    print(f"✅ API Key configurada: {api_key[:10]}...")
    
    # Conectar ao banco
    db = SessionLocal()
    
    try:
        # Inicializar gerador
        print("\n🔄 Inicializando gerador...")
        generator = HuggingFaceQuestionGenerator(db, api_key)
        
        # Teste de conexão
        print("\n🔄 Testando conexão...")
        connection_test = generator.test_connection()
        print(f"Status: {connection_test['status']}")
        if connection_test.get('model_used'):
            print(f"Modelo usado: {connection_test['model_used']}")
        if connection_test.get('response_preview'):
            print(f"Preview: {connection_test['response_preview']}")
        
        if connection_test['status'] != 'success':
            print("❌ Falha na conexão!")
            return
        
        # Buscar um tópico para teste
        print("\n🔄 Buscando tópico para teste...")
        topic = db.query(Topic).filter(Topic.disciplina == "Informática").first()
        
        if not topic:
            print("❌ Nenhum tópico de Informática encontrado!")
            print("💡 Execute: python criar_topicos.py")
            return
        
        print(f"✅ Tópico encontrado: {topic.disciplina} - {topic.topico}")
        
        # Gerar questão de teste
        print("\n🔄 Gerando questão de teste...")
        questions = generator.generate_questions_with_ai(topic, quantity=1)
        
        if questions:
            question = questions[0]
            print("\n✅ QUESTÃO GERADA COM SUCESSO!")
            print("=" * 50)
            print(f"📚 Disciplina: {question.disciplina}")
            print(f"📖 Tópico: {question.topico}")
            print(f"❓ Enunciado: {question.enunciado}")
            print(f"A) {question.alternativa_a}")
            print(f"B) {question.alternativa_b}")
            print(f"C) {question.alternativa_c}")
            print(f"D) {question.alternativa_d}")
            print(f"✅ Gabarito: {question.gabarito}")
            print(f"💡 Explicação: {question.explicacao_detalhada}")
            print(f"🎯 Fonte: {question.fonte}")
            print("=" * 50)
        else:
            print("❌ Falha ao gerar questão!")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        db.close()

def comparar_geradores():
    """Compara Gemini vs HuggingFace"""
    
    print("\n🆚 COMPARAÇÃO: GEMINI vs HUGGINGFACE")
    print("=" * 60)
    
    comparacao = {
        "Custo": {
            "Gemini": "Gratuito até quota (limitado)",
            "HuggingFace": "$0.10/mês (mais generoso)"
        },
        "Rate Limiting": {
            "Gemini": "Muito restritivo (20 req/dia)",
            "HuggingFace": "Mais flexível"
        },
        "Qualidade PT": {
            "Gemini": "Excelente",
            "HuggingFace": "Boa (modelos especializados)"
        },
        "Confiabilidade": {
            "Gemini": "Instável (quota esgota)",
            "HuggingFace": "Mais estável"
        },
        "Fallback": {
            "Gemini": "Limitado (poucos modelos)",
            "HuggingFace": "Excelente (muitos modelos)"
        }
    }
    
    for categoria, valores in comparacao.items():
        print(f"\n📊 {categoria}:")
        print(f"  🔵 Gemini: {valores['Gemini']}")
        print(f"  🟠 HuggingFace: {valores['HuggingFace']}")
    
    print("\n🎯 RECOMENDAÇÃO:")
    print("✅ HuggingFace é melhor para produção")
    print("✅ Mais estável e previsível")
    print("✅ Melhor custo-benefício")

if __name__ == "__main__":
    testar_huggingface()
    comparar_geradores()