#!/usr/bin/env python3
"""
Script para popular o usuário teste diretamente no Render via API.
"""
import requests
import json

API_URL = "https://simulados-ibgp.onrender.com"

def criar_usuario_teste():
    """Cria o usuário teste via API"""
    print("👤 Criando usuário teste...")
    
    try:
        # Dados do usuário
        user_data = {
            "email": "teste@example.com",
            "username": "teste",
            "password": "teste123",
            "full_name": "Usuário Teste"
        }
        
        # Tentar criar usuário
        response = requests.post(
            f"{API_URL}/api/register",
            json=user_data,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Usuário criado com sucesso!")
            return True
        elif response.status_code == 400 and "already" in response.text.lower():
            print("ℹ️ Usuário já existe (isso é bom!)")
            return True
        else:
            print("❌ Erro ao criar usuário")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return False

def testar_login():
    """Testa o login após criar o usuário"""
    print("🔐 Testando login...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/token",
            data={
                "username": "teste",
                "password": "teste123"
            },
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login realizado com sucesso!")
            print(f"Token recebido: {len(data.get('access_token', ''))} caracteres")
            return True
        else:
            print(f"❌ Erro no login: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("👤 CRIAÇÃO DE USUÁRIO NO RENDER")
    print("=" * 60)
    
    # Verificar API
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ API não está acessível")
            return
        print("✅ API está online")
    except:
        print("❌ API não está acessível")
        return
    
    # Criar usuário
    if criar_usuario_teste():
        print("\n" + "="*40)
        # Testar login
        if testar_login():
            print("\n✅ SUCESSO TOTAL!")
            print("Agora você pode fazer login no frontend:")
            print("- Usuário: teste")
            print("- Senha: teste123")
        else:
            print("\n❌ Login ainda falhou")
    else:
        print("\n❌ Falha ao criar usuário")

if __name__ == "__main__":
    main()