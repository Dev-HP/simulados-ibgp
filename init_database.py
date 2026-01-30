#!/usr/bin/env python3
"""
Inicializar banco de dados via API
"""
import requests

BASE_URL = "https://simulados-ibgp.onrender.com"

def init_database():
    print("🗄️  INICIALIZANDO BANCO DE DADOS")
    print("=" * 40)
    
    # Chamar endpoint de inicialização
    print("\n1. Criando tópicos e usuário...")
    try:
        response = requests.get(f"{BASE_URL}/api/initialize", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Banco inicializado!")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Mensagem: {data.get('message', 'N/A')}")
            
            if 'details' in data:
                details = data['details']
                print(f"   Tópicos: {details.get('topics', 'N/A')}")
                print(f"   Usuário: {details.get('user', 'N/A')}")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if init_database():
        print("\n✅ Banco pronto para uso!")
        print("\nAgora execute: python test_final.py")
    else:
        print("\n❌ Falha na inicialização")
