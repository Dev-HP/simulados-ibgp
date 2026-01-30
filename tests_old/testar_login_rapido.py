#!/usr/bin/env python3
"""
Teste rápido do login
"""
import requests

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

# Testar diferentes endpoints de login
endpoints = [
    "/auth/login",
    "/login", 
    "/users/login",
    "/auth/token"
]

for endpoint in endpoints:
    try:
        login_data = {"username": "teste", "password": "teste123"}
        response = requests.post(f"{API_URL}{endpoint}", json=login_data, timeout=10)
        print(f"{endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Login funcionando em {endpoint}")
            break
    except Exception as e:
        print(f"{endpoint}: Erro - {str(e)}")