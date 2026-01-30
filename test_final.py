#!/usr/bin/env python3
"""
Teste final do sistema após correções
"""
import requests
import time

BASE_URL = "https://simulados-ibgp.onrender.com"

def test_system():
    print("🧪 TESTE FINAL DO SISTEMA")
    print("=" * 40)
    
    # 1. Health check
    print("\n1. Health check...")
    try:
        r = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if r.status_code == 200:
            print("✅ API online")
        else:
            print(f"❌ API status: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ API offline: {e}")
        return False
    
    # 2. Initialize user
    print("\n2. Inicializando usuário...")
    try:
        requests.get(f"{BASE_URL}/api/seed-simple", timeout=10)
        print("✅ Usuário inicializado")
    except:
        pass
    
    # 3. Login
    print("\n3. Login...")
    try:
        login = requests.post(
            f"{BASE_URL}/api/token",
            data={"username": "teste", "password": "teste123"},
            timeout=10
        )
        if login.status_code == 200:
            token = login.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login OK")
        else:
            print(f"❌ Login falhou: {login.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return False
    
    # 4. Test HuggingFace generator
    print("\n4. Testando gerador HuggingFace...")
    try:
        # Primeiro, buscar um tópico válido
        topics_response = requests.get(f"{BASE_URL}/api/topics", headers=headers, timeout=10)
        
        if topics_response.status_code != 200:
            print("❌ Não foi possível buscar tópicos")
            return False
        
        topics = topics_response.json()
        if not topics:
            print("❌ Nenhum tópico encontrado")
            return False
        
        topic_id = topics[0]["id"]
        print(f"   Usando tópico ID: {topic_id}")
        
        test = requests.post(
            f"{BASE_URL}/api/generate-with-ai?topic_id={topic_id}&quantity=2&strategy=huggingface_only",
            headers=headers,
            timeout=60
        )
        
        if test.status_code == 200:
            data = test.json()
            generated = data.get("total_generated", 0)
            print(f"✅ Geradas: {generated} questões")
            print(f"   Estratégia: {data.get('strategy_used', 'N/A')}")
            return True
        elif test.status_code == 400:
            error = test.json().get("detail", "")
            if "HUGGINGFACE_API_KEY" in error:
                print("⚠️  API key não configurada no Render")
                print("   Configure HUGGINGFACE_API_KEY nas env vars")
                return False
            else:
                print(f"❌ Erro 400: {error}")
                return False
        elif test.status_code == 422:
            error = test.json()
            print(f"❌ Erro de validação (422)")
            print(f"   Detalhes: {error}")
            return False
        else:
            print(f"❌ Status: {test.status_code}")
            try:
                print(f"   Erro: {test.json()}")
            except:
                print(f"   Resposta: {test.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_system()
    print("\n" + "=" * 40)
    if success:
        print("✅ SISTEMA FUNCIONANDO!")
    else:
        print("❌ SISTEMA COM PROBLEMAS")
        print("\nPróximos passos:")
        print("1. Aguardar deploy completar (5-10 min)")
        print("2. Configurar HUGGINGFACE_API_KEY no Render")
        print("3. Executar este teste novamente")
