#!/usr/bin/env python3
"""
Teste final do endpoint após correção
"""
import requests
import time

def teste_final():
    """Teste final do endpoint corrigido"""
    print("🎯 TESTE FINAL - ENDPOINT CORRIGIDO")
    print("=" * 40)
    
    BASE_URL = "https://simulados-ibgp.onrender.com"
    
    # Aguardar um pouco para o servidor se estabilizar
    print("1. Aguardando servidor estabilizar...")
    time.sleep(10)
    
    # Verificar health
    print("\n2. Verificando health...")
    for tentativa in range(1, 4):
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=15)
            if response.status_code == 200:
                print(f"✅ API online (tentativa {tentativa})")
                break
            else:
                print(f"❌ Tentativa {tentativa}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Tentativa {tentativa}: {str(e)}")
            
        if tentativa < 3:
            time.sleep(10)
    
    # Login
    print("\n3. Fazendo login...")
    token = None
    
    for tentativa in range(1, 4):
        try:
            login_data = {"username": "teste", "password": "teste123"}
            response = requests.post(f"{BASE_URL}/api/token", data=login_data, timeout=20)
            
            if response.status_code == 200:
                token = response.json()["access_token"]
                print(f"✅ Login OK (tentativa {tentativa})")
                break
            else:
                print(f"❌ Tentativa {tentativa}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Tentativa {tentativa}: {str(e)}")
            
        if tentativa < 3:
            time.sleep(10)
    
    if not token:
        print("❌ Não foi possível fazer login")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Teste do endpoint corrigido
    print("\n4. Testando endpoint generate-complete-exam...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate-complete-exam",
            headers=headers,
            timeout=45
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 ENDPOINT FUNCIONANDO PERFEITAMENTE!")
            print(f"   Mensagem: {data.get('message', 'N/A')}")
            print(f"   Total gerado: {data.get('total_generated', 'N/A')}")
            print(f"   Estratégia: {data.get('strategy_used', 'N/A')}")
            
            if data.get('strategy_used') == 'huggingface_only':
                print("✅ CORREÇÃO CONFIRMADA: Usando HuggingFace!")
            
        elif response.status_code == 400:
            error = response.json()
            detail = error.get('detail', '')
            
            if 'HUGGINGFACE_API_KEY' in detail:
                print("🎉 CORREÇÃO APLICADA COM SUCESSO!")
                print("   ✅ Endpoint migrado do Gemini para HuggingFace")
                print("   ⚠️  Precisa configurar HUGGINGFACE_API_KEY no Render")
                print("\n📋 PRÓXIMOS PASSOS:")
                print("   1. Acessar dashboard do Render")
                print("   2. Ir em Environment Variables")
                print("   3. Adicionar: HUGGINGFACE_API_KEY=sua_chave_aqui")
                print("   4. Fazer redeploy")
                
            elif 'GEMINI_API_KEY' in detail:
                print("❌ CORREÇÃO NÃO APLICADA")
                print("   Endpoint ainda usa Gemini")
                
            else:
                print(f"⚠️  Erro 400 diferente: {detail}")
                
        elif response.status_code == 500:
            error = response.json()
            detail = error.get('detail', '')
            
            if 'GeminiQuestionGenerator' in detail:
                print("❌ CORREÇÃO NÃO APLICADA")
                print("   Ainda tem erro do GeminiQuestionGenerator")
                
            else:
                print(f"⚠️  Erro 500: {detail}")
                
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            print(f"   Resposta: {response.text[:300]}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - endpoint pode estar funcionando mas demorou muito")
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")

if __name__ == "__main__":
    teste_final()