#!/usr/bin/env python3
"""
Testa se o Gemini está funcionando em produção
"""
import requests

API_URL = "https://simulados-ibgp.onrender.com"

def testar_gemini_producao():
    print("🧪 TESTANDO GEMINI EM PRODUÇÃO")
    print("=" * 50)
    
    # 1. Login
    print("1. Fazendo login...")
    login_data = {"username": "teste", "password": "teste123"}
    response = requests.post(f"{API_URL}/api/token", data=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login falhou: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    print("✅ Login OK")
    
    # 2. Testar estatísticas do Gemini
    print("\n2. Verificando estatísticas do Gemini...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/api/gemini/stats", headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ Gemini configurado!")
        print(f"   Tier: {stats.get('tier', 'N/A')}")
        print(f"   Requisições hoje: {stats.get('requests_today', 'N/A')}")
        print(f"   Limite diário: {stats.get('daily_limit', 'N/A')}")
        return True
    else:
        print(f"❌ Gemini não configurado: {response.status_code}")
        if response.status_code == 500:
            print("   Provavelmente falta API key no Render")
        return False

if __name__ == "__main__":
    testar_gemini_producao()