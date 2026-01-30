#!/usr/bin/env python3
"""
Aguardar deploy e testar endpoint corrigido
"""
import requests
import time

def aguardar_deploy():
    """Aguarda o deploy e testa o endpoint"""
    print("⏳ AGUARDANDO DEPLOY NO RENDER")
    print("=" * 40)
    
    BASE_URL = "https://simulados-ibgp.onrender.com"
    
    print("1. Aguardando 3 minutos para o deploy...")
    for i in range(180, 0, -30):
        print(f"   Restam {i} segundos...")
        time.sleep(30)
    
    print("\n2. Verificando se API está respondendo...")
    
    for tentativa in range(1, 6):
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ API respondendo na tentativa {tentativa}")
                break
            else:
                print(f"❌ Tentativa {tentativa}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Tentativa {tentativa}: Erro - {str(e)}")
            
        if tentativa < 5:
            print("   Aguardando 30s...")
            time.sleep(30)
    
    print("\n3. Testando login...")
    try:
        login_data = {"username": "teste", "password": "teste123"}
        response = requests.post(f"{BASE_URL}/api/token", data=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login OK - Deploy funcionou!")
            
            # Teste rápido do endpoint corrigido
            print("\n4. Testando endpoint corrigido...")
            try:
                response = requests.post(
                    f"{BASE_URL}/api/generate-complete-exam",
                    headers=headers,
                    timeout=30
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("🎉 SUCESSO! Endpoint funcionando com HuggingFace!")
                elif response.status_code == 400:
                    error = response.json()
                    detail = error.get('detail', '')
                    if 'HUGGINGFACE_API_KEY' in detail:
                        print("✅ Endpoint corrigido! Agora pede HuggingFace API key")
                    else:
                        print(f"❌ Erro 400: {detail}")
                elif response.status_code == 500:
                    error = response.json()
                    detail = error.get('detail', '')
                    if 'GeminiQuestionGenerator' in detail:
                        print("❌ Ainda tem erro do Gemini - deploy pode não ter terminado")
                    else:
                        print(f"❌ Erro 500: {detail}")
                else:
                    print(f"❌ Status inesperado: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print("⏰ Timeout - endpoint pode estar funcionando mas demorou")
                
            except Exception as e:
                print(f"❌ Erro no teste: {str(e)}")
                
        else:
            print(f"❌ Login falhou: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no login: {str(e)}")
    
    print(f"\n🔗 Para testar manualmente:")
    print(f"   API: {BASE_URL}/docs")
    print(f"   Health: {BASE_URL}/api/health")
    print(f"   Login: {BASE_URL}/login")

if __name__ == "__main__":
    aguardar_deploy()