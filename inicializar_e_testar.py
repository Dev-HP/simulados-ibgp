#!/usr/bin/env python3
"""
Inicializa o banco e testa login automaticamente
"""

import requests
import time
import json

API_URL = "https://simulados-ibgp.onrender.com"

def print_step(step, msg):
    print(f"\n{'='*60}")
    print(f"[{step}] {msg}")
    print('='*60)

def initialize_database():
    """Inicializa o banco de dados"""
    print_step("1/4", "Inicializando banco de dados...")
    
    try:
        response = requests.get(f"{API_URL}/api/initialize", timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def test_login():
    """Testa login"""
    print_step("2/4", "Testando login...")
    
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
            token = data.get("access_token")
            print(f"✅ Login OK!")
            print(f"Token: {token[:30]}...")
            return token
        else:
            print(f"❌ Login falhou")
            print(f"Resposta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return None

def check_user_exists():
    """Verifica se usuário existe via endpoint seed-simple"""
    print_step("3/4", "Criando usuário via seed-simple...")
    
    try:
        response = requests.get(f"{API_URL}/api/seed-simple", timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"⚠️  Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def test_with_token(token):
    """Testa endpoint com token"""
    print_step("4/4", "Testando acesso autenticado...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/topics", headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            topics = response.json()
            print(f"✅ Tópicos encontrados: {len(topics)}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 INICIALIZAÇÃO E TESTE AUTOMÁTICO")
    print("="*60)
    print(f"API: {API_URL}")
    print(f"Credenciais: teste / teste123")
    
    # Passo 1: Inicializar banco
    if not initialize_database():
        print("\n⚠️  Inicialização falhou, tentando seed-simple...")
        check_user_exists()
    
    time.sleep(2)
    
    # Passo 2: Testar login
    token = test_login()
    
    if not token:
        print("\n❌ Login falhou mesmo após inicialização")
        print("\n📋 Diagnóstico:")
        print("1. Banco pode não estar inicializado corretamente")
        print("2. Senha pode estar incorreta")
        print("3. Usuário pode não existir")
        print("\n💡 Tente acessar manualmente:")
        print(f"   {API_URL}/api/initialize")
        print(f"   {API_URL}/api/seed-simple")
        return 1
    
    time.sleep(1)
    
    # Passo 3: Testar com token
    if test_with_token(token):
        print("\n" + "="*60)
        print("🎉 TUDO FUNCIONANDO!")
        print("="*60)
        print(f"\n✅ Sistema está operacional")
        print(f"✅ Login funcionando")
        print(f"✅ Autenticação OK")
        print(f"\n🌐 Acesse: {API_URL}/login")
        print(f"🔑 Login: teste / teste123")
        print("="*60 + "\n")
        return 0
    else:
        print("\n⚠️  Autenticação funcionou mas há problemas nos endpoints")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
