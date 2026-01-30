#!/usr/bin/env python3
import requests

def main():
    print("🧪 TESTE RÁPIDO DA API")
    
    # Login
    login_data = {"username": "teste", "password": "teste123"}
    response = requests.post("https://simulados-ibgp.onrender.com/api/token", data=login_data)
    
    if response.status_code != 200:
        print(f"❌ Erro no login: {response.status_code}")
        print(response.text)
        return
        
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login OK!")
    
    # Testar endpoints simples
    print("1. Testando /api/topics...")
    response = requests.get("https://simulados-ibgp.onrender.com/api/topics", headers=headers)
    print(f"   Status: {response.status_code} - {len(response.json())} tópicos")
    
    print("2. Testando /api/questions...")
    response = requests.get("https://simulados-ibgp.onrender.com/api/questions?limit=5", headers=headers)
    print(f"   Status: {response.status_code} - {len(response.json())} questões")
    
    print("3. Testando geração de 1 questão...")
    data = {"topic_id": 1, "quantity": 1}
    try:
        response = requests.post("https://simulados-ibgp.onrender.com/api/generate", 
                               json=data, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Erro: {response.text}")
    except requests.exceptions.Timeout:
        print("   ❌ Timeout - API key do Gemini inválida!")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    main()