#!/usr/bin/env python3
"""
Teste do Sistema HuggingFace-Only
Testa o sistema simplificado usando apenas HuggingFace
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Topic
from services.hybrid_ai_generator import HybridAIGenerator

def testar_huggingface_only():
    """Testa o sistema HuggingFace-only"""
    print("🟠 TESTE SISTEMA HUGGINGFACE-ONLY")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Verificar se API key está configurada
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            print("❌ HUGGINGFACE_API_KEY não configurada!")
            print("💡 Configure no arquivo .env:")
            print("   HUGGINGFACE_API_KEY=hf_...")
            return
        
        print(f"✅ API Key configurada: {api_key[:10]}...")
        
        # Inicializar gerador
        print("\n🔄 Inicializando gerador HuggingFace-only...")
        try:
            generator = HybridAIGenerator(db)
            print("✅ Gerador inicializado com sucesso")
        except Exception as e:
            print(f"❌ Erro na inicialização: {str(e)}")
            return
        
        # Testar status
        print("\n📊 Testando status...")
        status = generator.get_status()
        print(f"✅ Status obtido:")
        print(f"   - Modo: {status.get('mode', 'unknown')}")
        print(f"   - HuggingFace disponível: {status['huggingface_available']}")
        print(f"   - Gemini disponível: {status['gemini_available']}")
        print(f"   - Taxa de sucesso HF: {status['success_rates']['huggingface']:.1%}")
        
        # Testar conexão
        print("\n🔗 Testando conexão...")
        test_results = generator.test_all_generators()
        hf_result = test_results.get('huggingface', {})
        print(f"✅ Teste de conexão:")
        print(f"   - Status: {hf_result.get('status', 'unknown')}")
        print(f"   - Modelos disponíveis: {hf_result.get('available_models', 0)}")
        
        # Buscar tópico para teste
        print("\n📚 Buscando tópico para teste...")
        topic = db.query(Topic).filter(Topic.disciplina == "Informática").first()
        if not topic:
            print("❌ Nenhum tópico de Informática encontrado")
            return
        
        print(f"✅ Tópico encontrado: {topic.topico} ({topic.disciplina})")
        
        # Testar geração
        print("\n🧠 Testando geração de questão...")
        try:
            questions = generator.generate_questions_with_ai(
                topic=topic,
                quantity=1,
                reference_questions=[],
                difficulty=None,
                strategy="huggingface_only"
            )
            
            if questions:
                question = questions[0]
                print("✅ Questão gerada com sucesso!")
                print(f"   - ID: {question.id}")
                print(f"   - Enunciado: {question.enunciado[:80]}...")
                print(f"   - Gabarito: {question.gabarito}")
                print(f"   - Fonte: {question.fonte}")
            else:
                print("⚠️ Nenhuma questão foi gerada")
        
        except Exception as e:
            print(f"❌ Erro na geração: {str(e)}")
        
        # Estatísticas finais
        print("\n📊 Estatísticas finais:")
        final_status = generator.get_status()
        stats = final_status['stats']
        print(f"   - Sucessos: {stats['huggingface_success']}")
        print(f"   - Falhas: {stats['huggingface_failures']}")
        print(f"   - Total gerado: {stats['total_generated']}")
        
        success_rate = final_status['success_rates']['huggingface']
        print(f"   - Taxa de sucesso: {success_rate:.1%}")
        
        if success_rate > 0:
            print("\n🎉 SISTEMA HUGGINGFACE-ONLY FUNCIONANDO!")
        else:
            print("\n⚠️ Sistema precisa de ajustes")
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    testar_huggingface_only()