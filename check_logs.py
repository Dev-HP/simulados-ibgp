#!/usr/bin/env python3
"""
Verificar logs e status detalhado do gerador
"""
import requests

BASE_URL = "https://simulados-ibgp.onrender.com"

def check_status():
    print("🔍 VERIFICANDO STATUS DETALHADO")
    print("=" * 40)
    
    # Login
    login = requests.post(
        f"{BASE_URL}/api/token",
        data={"username": "teste", "password": "teste123"},
        timeout=10
    )
    
    if login.status_code != 200:
        print("❌ Login falhou")
        return
    
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Status dos geradores
    print("\n1. Status dos geradores AI...")
    try:
        response = requests.get(f"{BASE_URL}/api/ai-generators-status", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Status obtido")
            print(f"\nModo: {data.get('mode', 'N/A')}")
            
            # HuggingFace
            hf = data.get('generators', {}).get('huggingface', {})
            print(f"\n🤗 HuggingFace:")
            print(f"   Disponível: {hf.get('available', False)}")
            print(f"   API Key: {hf.get('api_key_configured', False)}")
            print(f"   Taxa sucesso: {hf.get('success_rate', 0)}%")
            
            test_result = hf.get('test_result', {})
            if test_result:
                print(f"   Teste: {test_result.get('status', 'N/A')}")
                if 'message' in test_result:
                    print(f"   Mensagem: {test_result['message']}")
                if 'error' in test_result:
                    print(f"   Erro: {test_result['error']}")
            
            # Stats
            stats = data.get('stats', {})
            if stats:
                print(f"\n📊 Estatísticas:")
                print(f"   Total tentativas: {stats.get('total_attempts', 0)}")
                print(f"   Sucessos: {stats.get('successful', 0)}")
                print(f"   Falhas: {stats.get('failed', 0)}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Testar geração real
    print("\n2. Testando geração real...")
    try:
        topics = requests.get(f"{BASE_URL}/api/topics", headers=headers, timeout=10).json()
        if topics:
            topic_id = topics[0]['id']
            
            response = requests.post(
                f"{BASE_URL}/api/generate-with-ai?topic_id={topic_id}&quantity=1&strategy=huggingface_only",
                headers=headers,
                timeout=90
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Geradas: {data.get('total_generated', 0)}")
                print(f"   Referências: {data.get('references_used', 0)}")
                
                status = data.get('generators_status', {})
                if status:
                    print(f"   HF disponível: {status.get('huggingface_available', False)}")
                    rates = status.get('success_rates', {})
                    print(f"   Taxa HF: {rates.get('huggingface', 0)}%")
            else:
                print(f"   Erro: {response.json()}")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    check_status()
