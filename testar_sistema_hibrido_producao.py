#!/usr/bin/env python3
"""
Teste do Sistema Híbrido em Produção
Testa todos os endpoints do sistema híbrido Gemini + HuggingFace
"""
import requests
import json
import time
from datetime import datetime

# URLs de produção
BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def test_health():
    """Testa se o sistema está online"""
    print("🔍 Testando saúde do sistema...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Sistema online e funcionando")
            return True
        else:
            print(f"❌ Sistema com problemas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {str(e)}")
        return False

def test_ai_generators_status():
    """Testa status dos geradores de IA"""
    print("\n🤖 Testando status dos geradores de IA...")
    try:
        response = requests.get(f"{API_URL}/ai-generators-status", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint de status funcionando")
            
            # Mostrar status dos geradores
            generators = data.get('generators', {})
            
            print("\n📊 STATUS DOS GERADORES:")
            for name, info in generators.items():
                status = "✅" if info.get('available') else "❌"
                api_key = "✅" if info.get('api_key_configured') else "❌"
                success_rate = info.get('success_rate', 0) * 100
                
                print(f"  {status} {name.upper()}:")
                print(f"    - API Key: {api_key}")
                print(f"    - Taxa de sucesso: {success_rate:.1f}%")
                
                test_result = info.get('test_result', {})
                if test_result:
                    print(f"    - Teste: {test_result.get('status', 'unknown')}")
            
            # Mostrar recomendações
            recommendations = data.get('recommendations', {})
            if recommendations:
                print("\n💡 RECOMENDAÇÕES:")
                for key, value in recommendations.items():
                    print(f"  - {key}: {value}")
            
            return data
        else:
            print(f"❌ Erro no endpoint: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao testar status: {str(e)}")
        return None

def test_generate_with_ai():
    """Testa geração de questões com IA híbrida"""
    print("\n🧠 Testando geração de questões com IA híbrida...")
    
    # Primeiro, vamos buscar um tópico disponível
    try:
        response = requests.get(f"{API_URL}/topics", timeout=10)
        if response.status_code != 200:
            print("❌ Não foi possível buscar tópicos")
            return False
        
        topics = response.json()
        if not topics:
            print("❌ Nenhum tópico encontrado")
            return False
        
        # Usar o primeiro tópico
        topic = topics[0]
        topic_id = topic['id']
        
        print(f"📝 Testando com tópico: {topic['topico']} ({topic['disciplina']})")
        
        # Testar diferentes estratégias
        strategies = ["auto", "huggingface_first", "gemini_first"]
        
        for strategy in strategies:
            print(f"\n🔄 Testando estratégia: {strategy}")
            
            payload = {
                "topic_id": topic_id,
                "quantity": 1,
                "difficulty": "MEDIO",
                "use_references": True,
                "strategy": strategy
            }
            
            try:
                response = requests.post(
                    f"{API_URL}/generate-with-ai",
                    params=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    generated = data.get('total_generated', 0)
                    
                    if generated > 0:
                        print(f"✅ Estratégia {strategy}: {generated} questão gerada")
                        
                        # Mostrar detalhes
                        generators_status = data.get('generators_status', {})
                        if generators_status:
                            print(f"    - Gemini disponível: {generators_status.get('gemini_available', False)}")
                            print(f"    - HuggingFace disponível: {generators_status.get('huggingface_available', False)}")
                    else:
                        print(f"⚠️ Estratégia {strategy}: Nenhuma questão gerada")
                        print(f"    Response: {response.text[:200]}")
                else:
                    print(f"❌ Estratégia {strategy}: HTTP {response.status_code}")
                    print(f"    Response: {response.text[:200]}")
                
                # Aguardar entre testes
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Erro na estratégia {strategy}: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral no teste de geração: {str(e)}")
        return False

def test_database_stats():
    """Testa estatísticas do banco de dados"""
    print("\n📊 Testando estatísticas do banco...")
    try:
        response = requests.get(f"{API_URL}/estatisticas-banco", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estatísticas obtidas com sucesso")
            
            total = data.get('total_questoes', 0)
            print(f"📝 Total de questões: {total}")
            
            por_disciplina = data.get('por_disciplina', {})
            if por_disciplina:
                print("📚 Por disciplina:")
                for disciplina, count in por_disciplina.items():
                    print(f"  - {disciplina}: {count} questões")
            
            return data
        else:
            print(f"❌ Erro nas estatísticas: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas: {str(e)}")
        return None

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DO SISTEMA HÍBRIDO EM PRODUÇÃO")
    print("=" * 50)
    print(f"🌐 URL: {BASE_URL}")
    print(f"⏰ Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Teste 1: Saúde do sistema
    if not test_health():
        print("\n❌ Sistema offline. Aguarde o deploy terminar.")
        return
    
    # Teste 2: Status dos geradores
    generators_status = test_ai_generators_status()
    
    # Teste 3: Estatísticas do banco
    db_stats = test_database_stats()
    
    # Teste 4: Geração com IA (só se tiver geradores disponíveis)
    if generators_status:
        generators = generators_status.get('generators', {})
        has_any_generator = any(
            gen.get('available', False) 
            for gen in generators.values()
        )
        
        if has_any_generator:
            test_generate_with_ai()
        else:
            print("\n⚠️ Nenhum gerador de IA disponível. Configure as API keys:")
            print("   - GEMINI_API_KEY")
            print("   - HUGGINGFACE_API_KEY")
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    if db_stats:
        total_questoes = db_stats.get('total_questoes', 0)
        print(f"📝 Questões no banco: {total_questoes}")
    
    if generators_status:
        generators = generators_status.get('generators', {})
        gemini_ok = generators.get('gemini', {}).get('available', False)
        huggingface_ok = generators.get('huggingface', {}).get('available', False)
        
        print(f"🔵 Gemini: {'✅ Funcionando' if gemini_ok else '❌ Indisponível'}")
        print(f"🟠 HuggingFace: {'✅ Funcionando' if huggingface_ok else '❌ Indisponível'}")
        
        if gemini_ok or huggingface_ok:
            print("🎉 Sistema híbrido funcionando!")
        else:
            print("⚠️ Configure as API keys para ativar a geração de IA")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    main()