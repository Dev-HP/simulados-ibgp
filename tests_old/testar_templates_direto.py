#!/usr/bin/env python3
"""
Teste direto do endpoint templates-provas
"""
import requests

API_URL = "https://simulados-ibgp.onrender.com"

def testar_templates():
    print("🧪 TESTANDO TEMPLATES DIRETO")
    print("=" * 50)
    
    # Teste sem autenticação
    print("1. Testando sem autenticação...")
    response = requests.get(f"{API_URL}/api/templates-provas")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Templates encontrados: {len(data.get('templates', []))}")
        for template in data.get('templates', []):
            print(f"  • {template.get('nome', 'N/A')}")
    else:
        print(f"❌ Erro: {response.text}")
    
    print("\n2. Testando health check...")
    response = requests.get(f"{API_URL}/api/health")
    print(f"Health Status: {response.status_code}")
    
if __name__ == "__main__":
    testar_templates()