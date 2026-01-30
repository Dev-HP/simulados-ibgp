#!/usr/bin/env python3
"""
Teste rápido do endpoint de templates
"""

import requests

API_URL = "https://simulados-ibgp.onrender.com"

def test_templates():
    print("🧪 TESTANDO TEMPLATES DE PROVA")
    print("="*50)
    
    # 1. Login
    print("1. Fazendo login...")
    login_data = {"username": "teste", "password": "teste123"}
    response = requests.post(f"{API_URL}/api/token", data=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login falhou: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    print("✅ Login OK")
    
    # 2. Testar templates
    print("2. Testando templates...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/api/templates-provas", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        templates = data.get("templates", [])
        print(f"✅ Templates encontrados: {len(templates)}")
        
        for t in templates:
            print(f"  • {t.get('nome')}: {t.get('total_questoes')} questões")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_templates()