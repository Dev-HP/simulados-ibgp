#!/usr/bin/env python3
"""
Verificar status do deploy
"""
import requests
import time

def verificar_deploy():
    """Verifica se o deploy foi aplicado"""
    print("🔍 VERIFICANDO STATUS DO DEPLOY")
    print("=" * 35)
    
    BASE_URL = "https://simulados-ibgp.onrender.com"
    
    # 1. Verificar se API está respondendo
    print("1. Verificando API...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=15)
        print(f"   Health check: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API está online")
        else:
            print("❌ API com problemas")
            return
            
    except Exception as e:
        print(f"❌ API não responde: {str(e)}")
        return
    
    # 2. Testar login
    print("\n2. Testando login...")
    try:
        login_data = {"username": "teste", "password": "teste123"}
        response = requests.post(f"{BASE_URL}/api/token", data=login_data, timeout=15)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login OK")
        else:
            print(f"❌ Login falhou: {response.status_code}")
            if response.status_code == 401:
                print("   Pode ser problema temporário do deploy")
            return
            
    except Exception as e:
        print(f"❌ Erro no login: {str(e)}")
        return
    
    # 3. Verificar se a correção foi aplicada
    print("\n3. Verificando correção...")
    try:
        # Testar endpoint que foi corrigido
        response = requests.post(
            f"{BASE_URL}/api/generate-complete-exam",
            headers=headers,
            timeout=20
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            error = response.json()
            detail = error.get('detail', '')
            
            if 'HUGGINGFACE_API_KEY' in detail:
                print("🎉 CORREÇÃO APLICADA!")
                print("   Endpoint agora usa HuggingFace em vez de Gemini")
                return True
                
            elif 'GEMINI_API_KEY' in detail:
                print("❌ Correção ainda não aplicada")
                print("   Endpoint ainda usa Gemini")
                return False
                
        elif response.status_code == 500:
            error = response.json()
            detail = error.get('detail', '')
            
            if 'GeminiQuestionGenerator' in detail:
                print("❌ Correção ainda não aplicada")
                print("   Ainda tem erro do GeminiQuestionGenerator")
                return False
            else:
                print("⚠️  Status incerto - erro 500 diferente")
                print(f"   Erro: {detail}")
                
        elif response.status_code == 200:
            print("🎉 FUNCIONOU COMPLETAMENTE!")
            return True
            
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        
    return False

if __name__ == "__main__":
    if verificar_deploy():
        print("\n✅ Deploy aplicado com sucesso!")
        print("🔗 Teste manual: https://simulados-ibgp.onrender.com/docs")
    else:
        print("\n⏳ Deploy ainda em progresso...")
        print("   Aguarde mais alguns minutos e teste novamente")