#!/usr/bin/env python3
"""
Teste completo do sistema híbrido Gemini + HuggingFace
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Topic
from services.hybrid_ai_generator import HybridAIGenerator

def testar_sistema_hibrido():
    """Testa o sistema híbrido completo"""
    
    print("🤖 TESTE SISTEMA HÍBRIDO: GEMINI + HUGGINGFACE")
    print("=" * 60)
    
    # Verificar configuração
    gemini_key = os.getenv('GEMINI_API_KEY')
    huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
    
    print("🔑 CONFIGURAÇÃO:")
    print(f"  Gemini API Key: {'✅ Configurada' if gemini_key else '❌ Não configurada'}")
    print(f"  HuggingFace API Key: {'✅ Configurada' if huggingface_key else '❌ Não configurada'}")
    
    if not gemini_key and not huggingface_key:
        print("\n❌ ERRO: Nenhuma API key configurada!")
        print("💡 Configure pelo menos uma no arquivo .env:")
        print("GEMINI_API_KEY=sua_chave_gemini")
        print("HUGGINGFACE_API_KEY=hf_sua_chave_huggingface")
        return
    
    # Conectar ao banco
    db = SessionLocal()
    
    try:
        # Inicializar gerador híbrido
        print("\n🔄 Inicializando gerador híbrido...")
        generator = HybridAIGenerator(db)
        
        # Status inicial
        status = generator.get_status()
        print(f"  Gemini disponível: {'✅' if status['gemini_available'] else '❌'}")
        print(f"  HuggingFace disponível: {'✅' if status['huggingface_available'] else '❌'}")
        
        # Teste de conexão
        print("\n🔄 Testando conexões...")
        test_results = generator.test_all_generators()
        
        for provider, result in test_results.items():
            status_icon = "✅" if result.get('status') == 'success' else "❌"
            print(f"  {provider.capitalize()}: {status_icon} {result.get('status', 'unknown')}")
            if result.get('error'):
                print(f"    Erro: {result['error'][:100]}")
        
        # Buscar tópicos para teste
        print("\n🔄 Buscando tópicos para teste...")
        topics = db.query(Topic).limit(3).all()
        
        if not topics:
            print("❌ Nenhum tópico encontrado!")
            print("💡 Execute: python criar_topicos.py")
            return
        
        print(f"✅ {len(topics)} tópicos encontrados")
        
        # Testar diferentes estratégias
        strategies = ["auto", "gemini_first", "huggingface_first"]
        
        for i, topic in enumerate(topics[:2]):  # Testar apenas 2 tópicos
            print(f"\n{'='*60}")
            print(f"🎯 TESTE {i+1}: {topic.disciplina} - {topic.topico}")
            print(f"{'='*60}")
            
            for strategy in strategies:
                if strategy == "gemini_first" and not status['gemini_available']:
                    continue
                if strategy == "huggingface_first" and not status['huggingface_available']:
                    continue
                
                print(f"\n🔄 Estratégia: {strategy}")
                
                try:
                    questions = generator.generate_questions_with_ai(
                        topic=topic,
                        quantity=1,
                        strategy=strategy
                    )
                    
                    if questions:
                        question = questions[0]
                        print("✅ SUCESSO!")
                        print(f"  📚 {question.disciplina}")
                        print(f"  ❓ {question.enunciado[:100]}...")
                        print(f"  ✅ Gabarito: {question.gabarito}")
                        print(f"  🎯 Fonte: {question.fonte}")
                    else:
                        print("❌ Falha na geração")
                
                except Exception as e:
                    print(f"❌ Erro: {str(e)[:100]}")
        
        # Estatísticas finais
        print(f"\n{'='*60}")
        print("📊 ESTATÍSTICAS FINAIS")
        print(f"{'='*60}")
        
        final_status = generator.get_status()
        stats = final_status['stats']
        rates = final_status['success_rates']
        
        print(f"🔵 Gemini:")
        print(f"  Sucessos: {stats['gemini_success']}")
        print(f"  Falhas: {stats['gemini_failures']}")
        print(f"  Taxa de sucesso: {rates['gemini']:.1%}")
        
        print(f"🟠 HuggingFace:")
        print(f"  Sucessos: {stats['huggingface_success']}")
        print(f"  Falhas: {stats['huggingface_failures']}")
        print(f"  Taxa de sucesso: {rates['huggingface']:.1%}")
        
        # Recomendações
        print(f"\n🎯 RECOMENDAÇÕES:")
        if rates['huggingface'] > rates['gemini']:
            print("✅ HuggingFace está performando melhor")
            print("💡 Use strategy='huggingface_first' para melhor resultado")
        elif rates['gemini'] > rates['huggingface']:
            print("✅ Gemini está performando melhor")
            print("💡 Use strategy='gemini_first' para melhor resultado")
        else:
            print("✅ Ambos estão performando igualmente")
            print("💡 Use strategy='auto' para balanceamento automático")
    
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    
    finally:
        db.close()

def mostrar_configuracao():
    """Mostra como configurar as API keys"""
    
    print("\n🔧 COMO CONFIGURAR AS API KEYS")
    print("=" * 50)
    
    print("\n1️⃣ GEMINI (Google):")
    print("  🔗 https://makersuite.google.com/app/apikey")
    print("  📝 Adicione no .env: GEMINI_API_KEY=AIzaSy...")
    print("  💰 Gratuito: 15 req/min, 1500 req/dia")
    
    print("\n2️⃣ HUGGINGFACE:")
    print("  🔗 https://huggingface.co/settings/tokens")
    print("  📝 Adicione no .env: HUGGINGFACE_API_KEY=hf_...")
    print("  💰 Gratuito: $0.10/mês de créditos")
    
    print("\n3️⃣ RECOMENDAÇÃO:")
    print("  ✅ Configure AMBAS para máxima confiabilidade")
    print("  ✅ HuggingFace como backup do Gemini")
    print("  ✅ Sistema híbrido escolhe automaticamente")

if __name__ == "__main__":
    testar_sistema_hibrido()
    mostrar_configuracao()