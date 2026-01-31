#!/usr/bin/env python3
"""
Testa acesso ao frontend e backend
"""
import requests

BACKEND = "https://simulados-ibgp.onrender.com"
FRONTEND = "https://simulados-ibgp-1.onrender.com"

print("🔍 Testando acesso aos serviços...\n")

# Teste 1: Backend health
print("1️⃣ Backend Health Check:")
try:
    response = requests.get(f"{BACKEND}/health", timeout=10)
    if response.status_code == 200:
        print(f"   ✅ Backend OK: {response.json()}")
    else:
        print(f"   ❌ Backend erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {str(e)}")

# Teste 2: API Questions
print("\n2️⃣ API Questions:")
try:
    response = requests.get(f"{BACKEND}/api/questions?limit=5", timeout=10)
    if response.status_code == 200:
        questions = response.json()
        print(f"   ✅ API OK: {len(questions)} questões retornadas")
        
        # Verificar CORS headers
        headers = response.headers
        cors_origin = headers.get('access-control-allow-origin', 'NOT SET')
        print(f"   🔒 CORS Origin: {cors_origin}")
    else:
        print(f"   ❌ API erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {str(e)}")

# Teste 3: Frontend
print("\n3️⃣ Frontend:")
try:
    response = requests.get(FRONTEND, timeout=10)
    if response.status_code == 200:
        print(f"   ✅ Frontend OK (status {response.status_code})")
    else:
        print(f"   ⚠️  Frontend status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {str(e)}")

# Teste 4: Login endpoint
print("\n4️⃣ Login Page:")
try:
    response = requests.get(f"{BACKEND}/login", timeout=10)
    if response.status_code == 200:
        print(f"   ✅ Login page OK")
    else:
        print(f"   ❌ Login erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {str(e)}")

print("\n" + "=" * 60)
print("📝 RESUMO:")
print("=" * 60)
print(f"Backend:  {BACKEND}")
print(f"Frontend: {FRONTEND}")
print(f"Login:    teste / teste123")
print(f"Questões: 160 disponíveis")
print("=" * 60)
