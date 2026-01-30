#!/usr/bin/env python3
"""
Teste pós-deploy para verificar se a correção funcionou
"""
import requests

def teste_pos_deploy():
    """Testa se o deploy da correção funcionou"""
    print("✅ TESTE PÓS-DEPLOY - CORREÇÃO APLICADA?")
    print("=" * 45)
    
    BASE_URL = "https://simulados-ibgp.onrender.com"
    
    # 1. Verificar se API está online
    print("1. Verificando API...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ API online")
        else:
            print(f"❌ API com problema: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API não responde: {str(e)}")
        return
    
    # 2. Tentar login várias vezes (pode ter delay pós-deploy)
    print("\n2. Testando login...")
    token = None
    
    for tentativa in range(1, 4):
        try:
            login_data = {"username": "teste", "password": "teste123"}
            response = requests.post(f"{BASE_URL}/api/token", data=login_data, timeout=15)
            
            if response.status_code == 200:
                token = response.json()["access_token"]
                print(f"✅ Login OK (tentativa {tentativa})")
                break
            else:
                print(f"❌ Tentativa {tentativa}: {response.status_code}")
                if tentativa < 3:
                    import time
                    time.sleep(5)
                    
        except Exception as e:
            print(f"❌ Tentativa {tentativa}: {str(e)}")
            if tentativa < 3:
                import time
                time.sleep(5)
    
    if not token:
        print("❌ Não foi possível fazer login")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Testar o endpoint corrigido
    print("\n3. Testando endpoint corrigido...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate-complete-exam",
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 FUNCIONOU PERFEITAMENTE!")
            print(f"   Geradas: {data.get('total_generated', 0)}")
            print(f"   Estratégia: {data.get('strategy_used', 'N/A')}")
            
        elif response.status_code == 400:
            error = response.json()
            detail = error.get('detail', '')
            
            if 'HUGGINGFACE_API_KEY' in detail:
                print("🎉 CORREÇÃO APLICADA COM SUCESSO!")
                print("   ✅ Endpoint agora usa HuggingFace (não mais Gemini)")
                print("   ⚠️  Precisa configurar HUGGINGFACE_API_KEY no Render")
                
            elif 'GEMINI_API_KEY' in detail:
                print("❌ Correção NÃO foi aplicada")
                print("   Endpoint ainda usa Gemini")
                
            else:
                print(f"⚠️  Erro 400 diferente: {detail}")
                
        elif response.status_code == 500:
            error = response.json()
            detail = error.get('detail', '')
            
            if 'GeminiQuestionGenerator' in detail:
                print("❌ Correção NÃO foi aplicada")
                print("   Ainda tem erro do GeminiQuestionGenerator")
                
            else:
                print(f"⚠️  Erro 500 diferente: {detail}")
                
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
    
    # 4. Verificar outros endpoints relacionados
    print("\n4. Verificando outros endpoints...")
    
    endpoints_teste = [
        ("GET", "/ai-generators-status", "Status geradores"),
        ("GET", "/topics", "Listar tópicos")
    ]
    
    for method, endpoint, desc in endpoints_teste:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}/api{endpoint}", headers=headers, timeout=10)
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"   {status_icon} {method} {endpoint}: {response.status_code} - {desc}")
            
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: ERRO - {str(e)}")

if __name__ == "__main__":
    teste_pos_deploy()