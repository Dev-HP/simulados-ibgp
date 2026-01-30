#!/usr/bin/env python3
"""
Teste direto do endpoint de geração de questões
"""
import requests
import json

def main():
    print("🧪 TESTANDO ENDPOINT DIRETO")
    print("=" * 50)
    
    # URL da API
    api_url = "https://simulados-ibgp.onrender.com"
    
    # 1. Fazer login
    print("1. Fazendo login...")
    login_data = {
        "username": "teste",
        "password": "teste123"
    }
    
    try:
        response = requests.post(f"{api_url}/api/token", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ Login OK! Token: {token[:20]}...")
            
            # 2. Testar endpoint de geração
            print("\n2. Testando endpoint de geração...")
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.post(
                f"{api_url}/api/generate-complete-exam",
                headers=headers,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("✅ Endpoint funcionando!")
                print(f"Questões geradas: {result.get('total_generated', 0)}")
                print(f"Tempo: {result.get('total_time', 0)} segundos")
            else:
                print(f"❌ Erro: {response.text}")
                
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    main()