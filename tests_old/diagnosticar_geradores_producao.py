#!/usr/bin/env python3
"""
Diagnóstico detalhado dos geradores de IA em produção
"""
import requests
import json
import time

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def diagnosticar_geradores():
    """Diagnóstico completo dos geradores"""
    print("🔍 DIAGNÓSTICO DOS GERADORES DE IA")
    print("=" * 50)
    
    # 1. Status detalhado
    print("📊 Status dos geradores...")
    try:
        response = requests.get(f"{API_URL}/ai-generators-status", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Status obtido com sucesso")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro no status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    # 2. Teste de geração simples
    print("\n🧪 Teste de geração simples...")
    try:
        # Buscar primeiro tópico
        response = requests.get(f"{API_URL}/topics", timeout=10)
        if response.status_code == 200:
            topics = response.json()
            if topics:
                topic = topics[0]
                topic_id = topic['id']
                
                print(f"📝 Tópico: {topic['topico']} (ID: {topic_id})")
                
                # Teste com diferentes estratégias
                strategies = ["huggingface_only", "gemini_only"]
                
                for strategy in strategies:
                    print(f"\n🔄 Testando {strategy}...")
                    
                    payload = {
                        "topic_id": topic_id,
                        "quantity": 1,
                        "difficulty": "FACIL",
                        "use_references": False,
                        "strategy": strategy
                    }
                    
                    try:
                        response = requests.post(
                            f"{API_URL}/generate-with-ai",
                            params=payload,
                            timeout=120  # 2 minutos
                        )
                        
                        print(f"   Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            data = response.json()
                            print(f"   Geradas: {data.get('total_generated', 0)}")
                            print(f"   Estratégia: {data.get('strategy_used', 'N/A')}")
                            
                            generators = data.get('generators_status', {})
                            print(f"   Gemini disponível: {generators.get('gemini_available', False)}")
                            print(f"   HuggingFace disponível: {generators.get('huggingface_available', False)}")
                        else:
                            print(f"   Erro: {response.text[:300]}")
                    
                    except requests.exceptions.Timeout:
                        print(f"   ⏰ Timeout após 2 minutos")
                    except Exception as e:
                        print(f"   ❌ Erro: {str(e)}")
            else:
                print("❌ Nenhum tópico encontrado")
        else:
            print(f"❌ Erro ao buscar tópicos: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
    
    # 3. Verificar variáveis de ambiente (indiretamente)
    print("\n🔧 Verificando configuração...")
    try:
        response = requests.get(f"{API_URL}/ai-generators-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            generators = data.get('generators', {})
            
            gemini = generators.get('gemini', {})
            huggingface = generators.get('huggingface', {})
            
            print("🔵 GEMINI:")
            print(f"   - API Key configurada: {gemini.get('api_key_configured', False)}")
            print(f"   - Disponível: {gemini.get('available', False)}")
            print(f"   - Teste: {gemini.get('test_result', {})}")
            
            print("🟠 HUGGINGFACE:")
            print(f"   - API Key configurada: {huggingface.get('api_key_configured', False)}")
            print(f"   - Disponível: {huggingface.get('available', False)}")
            print(f"   - Teste: {huggingface.get('test_result', {})}")
    except Exception as e:
        print(f"❌ Erro na verificação: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 DIAGNÓSTICO CONCLUÍDO")

if __name__ == "__main__":
    diagnosticar_geradores()