#!/usr/bin/env python3
"""
Verificar se o usuário de teste existe
"""
import requests

def verificar_usuario():
    """Verifica se o usuário de teste existe"""
    print("👤 VERIFICANDO USUÁRIO DE TESTE")
    print("=" * 35)
    
    BASE_URL = "https://simulados-ibgp.onrender.com"
    
    # 1. Verificar se endpoint de inicialização existe
    print("1. Verificando endpoint de inicialização...")
    try:
        response = requests.get(f"{BASE_URL}/api/initialize", timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint de inicialização funciona")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Mensagem: {data.get('message', 'N/A')}")
            
            if 'details' in data:
                details = data['details']
                print(f"   Tópicos: {details.get('topics', 'N/A')}")
                print(f"   Usuário: {details.get('user', 'N/A')}")
                
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    # 2. Tentar criar usuário via seed-simple
    print("\n2. Tentando criar usuário via seed-simple...")
    try:
        response = requests.get(f"{BASE_URL}/api/seed-simple", timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Seed-simple executado")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Mensagem: {data.get('message', 'N/A')}")
            
            if 'credentials' in data:
                creds = data['credentials']
                print(f"   Username: {creds.get('username', 'N/A')}")
                print(f"   Password: {creds.get('password', 'N/A')}")
                
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    # 3. Tentar login após seed
    print("\n3. Tentando login após seed...")
    try:
        login_data = {"username": "teste", "password": "teste123"}
        response = requests.post(f"{BASE_URL}/api/token", data=login_data, timeout=15)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login funcionou!")
            token = response.json()["access_token"]
            print(f"   Token obtido: {token[:20]}...")
            
            # Agora testar o endpoint corrigido
            print("\n4. Testando endpoint corrigido...")
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.post(
                f"{BASE_URL}/api/generate-complete-exam",
                headers=headers,
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 400:
                error = response.json()
                detail = error.get('detail', '')
                
                if 'HUGGINGFACE_API_KEY' in detail:
                    print("🎉 CORREÇÃO FUNCIONOU!")
                    print("   Endpoint agora usa HuggingFace")
                elif 'GEMINI_API_KEY' in detail:
                    print("❌ Correção não aplicada - ainda usa Gemini")
                else:
                    print(f"   Erro: {detail}")
                    
            elif response.status_code == 500:
                error = response.json()
                detail = error.get('detail', '')
                if 'GeminiQuestionGenerator' in detail:
                    print("❌ Correção não aplicada - erro do Gemini")
                else:
                    print(f"   Erro 500: {detail}")
                    
            else:
                print(f"   Status inesperado: {response.status_code}")
                
        else:
            error_data = response.json() if response.status_code != 500 else {}
            print(f"❌ Login falhou: {error_data.get('detail', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"❌ Erro no login: {str(e)}")

if __name__ == "__main__":
    verificar_usuario()