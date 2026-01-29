#!/usr/bin/env python3
"""
Script para testar o login e verificar se o usuário existe.
"""
import requests
import json

API_URL = "https://simulados-ibgp.onrender.com"

def testar_login():
    """Testa o login com as credenciais corretas"""
    print("🔐 Testando login...")
    
    try:
        # Testar login
        response = requests.post(
            f"{API_URL}/api/token",
            data={
                "username": "teste",
                "password": "teste123"
            },
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login realizado com sucesso!")
            print(f"Token: {data.get('access_token', 'N/A')[:50]}...")
            return data.get('access_token')
        else:
            print("❌ Erro no login")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return None

def verificar_api():
    """Verifica se a API está respondendo"""
    print("🔍 Verificando API...")
    
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        print(f"Health check: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API está online")
            return True
        else:
            print("❌ API com problemas")
            return False
            
    except Exception as e:
        print(f"❌ API não acessível: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTE DE LOGIN")
    print("=" * 60)
    
    # Verificar API
    if not verificar_api():
        print("❌ API não está acessível. Verifique o deploy.")
        return
    
    # Testar login
    token = testar_login()
    
    if token:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("O login está funcionando corretamente.")
    else:
        print("\n❌ TESTE FALHOU!")
        print("Verifique se o usuário 'teste' existe no banco.")
        print("Execute: python api/scripts/seed_database.py")

if __name__ == "__main__":
    main()