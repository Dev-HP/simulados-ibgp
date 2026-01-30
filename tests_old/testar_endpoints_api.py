#!/usr/bin/env python3
"""
Testar endpoints disponíveis na API
"""
import requests

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def testar_endpoints():
    """Testa endpoints disponíveis"""
    print("🔍 TESTANDO ENDPOINTS DA API")
    print("=" * 40)
    
    # Fazer login
    login_data = {"username": "teste", "password": "teste123"}
    response = requests.post(f"{API_URL}/token", data=login_data, timeout=10)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login OK")
    else:
        print("❌ Erro no login")
        return
    
    # Testar endpoints
    endpoints = [
        ("GET", "/topics", "Listar tópicos"),
        ("GET", "/questions", "Listar questões"),
        ("POST", "/questions/generate-with-ai", "Gerar com IA"),
        ("GET", "/questions/ai-generators-status", "Status geradores"),
        ("POST", "/questions/generate-complete-exam", "Prova completa"),
        ("GET", "/estatisticas-banco", "Estatísticas banco")
    ]
    
    for method, endpoint, desc in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{API_URL}{endpoint}", headers=headers, timeout=10)
            else:
                response = requests.post(f"{API_URL}{endpoint}", headers=headers, timeout=10)
            
            print(f"{method} {endpoint}: {response.status_code} - {desc}")
            
            if response.status_code == 200 and endpoint == "/topics":
                data = response.json()
                print(f"   📊 {len(data)} tópicos encontrados")
                if data:
                    print(f"   📝 Primeiro: {data[0].get('disciplina')} - {data[0].get('topico')}")
                    
        except Exception as e:
            print(f"{method} {endpoint}: ERRO - {str(e)}")

if __name__ == "__main__":
    testar_endpoints()