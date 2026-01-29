#!/usr/bin/env python3
"""
Popula o banco com questões de exemplo AGORA
"""

import requests
import time

API_URL = "https://simulados-ibgp.onrender.com"

print("="*60)
print("🚀 POPULANDO BANCO COM QUESTÕES")
print("="*60)

print("\n[1/2] Chamando endpoint seed-database...")
try:
    response = requests.get(f"{API_URL}/api/seed-database", timeout=60)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso!")
        print(f"   Questões criadas: {data.get('data', {}).get('questions', 0)}")
    else:
        print(f"⚠️  Resposta: {response.text}")
except Exception as e:
    print(f"❌ Erro: {str(e)}")

time.sleep(2)

print("\n[2/2] Verificando questões...")
try:
    # Login
    token_response = requests.post(
        f"{API_URL}/api/token",
        data={"username": "teste", "password": "teste123"},
        timeout=10
    )
    
    if token_response.status_code == 200:
        token = token_response.json()["access_token"]
        
        # Buscar questões
        headers = {"Authorization": f"Bearer {token}"}
        questions_response = requests.get(
            f"{API_URL}/api/questions",
            headers=headers,
            timeout=10
        )
        
        if questions_response.status_code == 200:
            questions = questions_response.json()
            print(f"✅ Total de questões no banco: {len(questions)}")
            
            if len(questions) > 0:
                print(f"\n📋 Exemplos:")
                for i, q in enumerate(questions[:3], 1):
                    print(f"   {i}. {q.get('disciplina')} - {q.get('topico')}")
        else:
            print(f"❌ Erro ao buscar questões: {questions_response.status_code}")
    else:
        print(f"❌ Erro no login: {token_response.status_code}")
        
except Exception as e:
    print(f"❌ Erro: {str(e)}")

print("\n" + "="*60)
print("✅ PRONTO!")
print("="*60)
print("\n🌐 Acesse agora:")
print(f"   {API_URL}/ai-generator")
print("\n💡 Ou gere mais questões com IA no sistema!")
print("="*60 + "\n")
