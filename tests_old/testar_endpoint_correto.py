#!/usr/bin/env python3
"""
Testar o endpoint correto para gerar 60 questões
"""
import requests
import json

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def testar_endpoint_60_questoes():
    """Testa o endpoint correto para gerar 60 questões"""
    print("🔍 TESTANDO ENDPOINT CORRETO PARA 60 QUESTÕES")
    print("=" * 50)
    
    # Fazer login
    print("1. Fazendo login...")
    login_data = {"username": "teste", "password": "teste123"}
    
    try:
        response = requests.post(f"{API_URL}/token", data=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login realizado com sucesso")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Erro na conexão de login: {str(e)}")
        return
    
    # Testar endpoint correto
    print("\n2. Testando endpoint correto...")
    endpoint_correto = "/questions/generate-complete-exam"
    
    try:
        print(f"   Chamando: POST {API_URL}{endpoint_correto}")
        response = requests.post(
            f"{API_URL}{endpoint_correto}", 
            headers=headers, 
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funciona!")
            print(f"   Mensagem: {data.get('message', 'N/A')}")
            print(f"   Total gerado: {data.get('total_generated', 'N/A')}")
            print(f"   Esperado: {data.get('expected', 'N/A')}")
            
            if 'report' in data:
                print("\n📊 Relatório por disciplina:")
                for disciplina, topicos in data['report'].items():
                    total_disciplina = sum(topicos.values()) if isinstance(topicos, dict) else topicos
                    print(f"   {disciplina}: {total_disciplina} questões")
                    
        elif response.status_code == 400:
            error_data = response.json()
            print(f"❌ Erro 400: {error_data.get('detail', 'Erro desconhecido')}")
            
        elif response.status_code == 500:
            error_data = response.json()
            print(f"❌ Erro 500: {error_data.get('detail', 'Erro interno')}")
            
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - O endpoint pode estar funcionando mas demorou mais que 30s")
        print("   Isso é normal para geração de 60 questões (pode levar 15-20 min)")
        
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
    
    # Testar endpoints relacionados
    print("\n3. Testando endpoints relacionados...")
    
    endpoints_relacionados = [
        ("GET", "/questions/ai-generators-status", "Status dos geradores"),
        ("GET", "/prova-completa/estatisticas-banco", "Estatísticas do banco"),
        ("GET", "/prova-completa/templates-provas", "Templates de provas")
    ]
    
    for method, endpoint, desc in endpoints_relacionados:
        try:
            if method == "GET":
                response = requests.get(f"{API_URL}{endpoint}", headers=headers, timeout=10)
            else:
                response = requests.post(f"{API_URL}{endpoint}", headers=headers, timeout=10)
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"   {status_icon} {method} {endpoint}: {response.status_code} - {desc}")
            
            if response.status_code == 200 and "estatisticas" in endpoint:
                data = response.json()
                total = data.get('total_questoes', 0)
                print(f"      📊 Total de questões no banco: {total}")
                
        except Exception as e:
            print(f"   ❌ {method} {endpoint}: ERRO - {str(e)}")

if __name__ == "__main__":
    testar_endpoint_60_questoes()