#!/usr/bin/env python3
"""
Teste simples e direto do endpoint
"""
import requests

def teste_simples():
    """Teste simples do endpoint"""
    print("🔍 TESTE SIMPLES - ENDPOINT 60 QUESTÕES")
    print("=" * 40)
    
    BASE_URL = "https://simulados-ibgp.onrender.com/api"
    
    # Login
    print("1. Login...")
    login_data = {"username": "teste", "password": "teste123"}
    
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_data, timeout=15)
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login OK")
        else:
            print(f"❌ Login falhou: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro no login: {str(e)}")
        return
    
    # Teste direto do endpoint
    print("\n2. Testando endpoint...")
    
    try:
        # Primeiro, verificar se o endpoint existe com OPTIONS
        response = requests.options(f"{BASE_URL}/generate-complete-exam", headers=headers, timeout=10)
        print(f"   OPTIONS: {response.status_code}")
        
        # Testar POST
        response = requests.post(f"{BASE_URL}/generate-complete-exam", headers=headers, timeout=60)
        print(f"   POST: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ FUNCIONOU!")
            data = response.json()
            print(f"   Geradas: {data.get('total_generated', 'N/A')}")
            
        elif response.status_code == 405:
            print("❌ Método não permitido")
            print("   O endpoint pode estar definido incorretamente")
            
        elif response.status_code == 422:
            print("❌ Erro de validação")
            error = response.json()
            print(f"   Detalhes: {error}")
            
        elif response.status_code == 500:
            print("❌ Erro interno do servidor")
            try:
                error = response.json()
                print(f"   Detalhes: {error.get('detail', 'Sem detalhes')}")
            except:
                print(f"   Resposta: {response.text[:200]}")
                
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - pode estar funcionando mas demorou muito")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    teste_simples()