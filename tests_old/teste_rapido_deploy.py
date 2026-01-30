#!/usr/bin/env python3
"""
Teste rápido para verificar se deploy foi aplicado
"""
import requests

def teste_rapido():
    """Teste rápido do deploy"""
    print("🚀 TESTE RÁPIDO - DEPLOY APLICADO?")
    print("=" * 40)
    
    BASE_URL = "https://simulados-ibgp.onrender.com/api"
    
    # Login
    try:
        login_data = {"username": "teste", "password": "teste123"}
        response = requests.post(f"{BASE_URL}/token", data=login_data, timeout=10)
        
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
    
    # Teste do endpoint
    try:
        response = requests.post(
            f"{BASE_URL}/generate-complete-exam",
            headers=headers,
            timeout=15
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 FUNCIONOU! Deploy aplicado com sucesso!")
            
        elif response.status_code == 400:
            error = response.json()
            detail = error.get('detail', '')
            if 'HUGGINGFACE_API_KEY' in detail:
                print("✅ DEPLOY APLICADO! Agora pede HuggingFace API key")
                print("   (Isso significa que a correção funcionou)")
            elif 'GEMINI_API_KEY' in detail:
                print("❌ Deploy ainda não aplicado - ainda pede Gemini")
            else:
                print(f"❌ Erro 400: {detail}")
                
        elif response.status_code == 500:
            error = response.json()
            detail = error.get('detail', '')
            if 'GeminiQuestionGenerator' in detail:
                print("❌ Deploy ainda não aplicado - ainda usa Gemini")
            else:
                print(f"✅ Deploy pode ter sido aplicado - erro diferente: {detail}")
                
        else:
            print(f"Status inesperado: {response.status_code}")
            print(f"Resposta: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    teste_rapido()