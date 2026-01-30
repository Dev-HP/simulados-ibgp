#!/usr/bin/env python3
"""
Teste do login com endpoint correto
"""
import requests

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def testar_login():
    """Testa o login com o endpoint correto"""
    print("🔐 TESTANDO LOGIN")
    print("=" * 30)
    
    # Dados do login (OAuth2PasswordRequestForm usa form data)
    login_data = {
        "username": "teste",
        "password": "teste123"
    }
    
    try:
        # Usar form data, não JSON
        response = requests.post(f"{API_URL}/token", data=login_data, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Login realizado com sucesso!")
            print(f"Token: {token[:50]}...")
            
            # Testar endpoint protegido
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{API_URL}/users/me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Endpoint protegido funcionando!")
                print(f"Usuário: {user_data.get('username')} ({user_data.get('full_name')})")
            else:
                print(f"⚠️ Problema no endpoint protegido: {response.status_code}")
                
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    testar_login()