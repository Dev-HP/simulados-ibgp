#!/usr/bin/env python3
"""
Diagnosticar problema com endpoint de 60 questões
"""
import requests
import json

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def diagnosticar_endpoint():
    """Diagnostica o problema com o endpoint de 60 questões"""
    print("🔍 DIAGNÓSTICO COMPLETO - ENDPOINT 60 QUESTÕES")
    print("=" * 50)
    
    # 1. Fazer login
    print("1. Fazendo login...")
    try:
        login_data = {"username": "teste", "password": "teste123"}
        response = requests.post(f"{API_URL}/token", data=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login OK")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return
    
    # 2. Verificar pré-requisitos
    print("\n2. Verificando pré-requisitos...")
    
    # Verificar se há tópicos
    try:
        response = requests.get(f"{API_URL}/topics", headers=headers, timeout=10)
        if response.status_code == 200:
            topics = response.json()
            print(f"✅ Tópicos: {len(topics)} encontrados")
            if topics:
                print(f"   Exemplo: {topics[0].get('disciplina')} - {topics[0].get('topico')}")
        else:
            print(f"❌ Erro ao buscar tópicos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar tópicos: {str(e)}")
    
    # Verificar status dos geradores
    try:
        response = requests.get(f"{API_URL}/ai-generators-status", headers=headers, timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✅ Status dos geradores obtido")
            
            # Verificar HuggingFace
            hf_status = status.get('generators', {}).get('huggingface', {})
            hf_available = hf_status.get('available', False)
            hf_api_key = hf_status.get('api_key_configured', False)
            
            print(f"   HuggingFace disponível: {hf_available}")
            print(f"   HuggingFace API key: {hf_api_key}")
            
            if not hf_available or not hf_api_key:
                print("⚠️  PROBLEMA: HuggingFace não está configurado corretamente")
                
        else:
            print(f"❌ Erro ao verificar geradores: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar geradores: {str(e)}")
    
    # 3. Testar endpoint com diferentes métodos
    print("\n3. Testando endpoint generate-complete-exam...")
    
    endpoint = "/generate-complete-exam"
    
    # Testar GET
    try:
        response = requests.get(f"{API_URL}{endpoint}", headers=headers, timeout=10)
        print(f"   GET {endpoint}: {response.status_code}")
        if response.status_code != 405:
            print(f"      Resposta: {response.text[:100]}...")
    except Exception as e:
        print(f"   GET {endpoint}: ERRO - {str(e)}")
    
    # Testar POST sem dados
    try:
        response = requests.post(f"{API_URL}{endpoint}", headers=headers, timeout=30)
        print(f"   POST {endpoint} (sem dados): {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCESSO! Endpoint funcionou")
            print(f"      Mensagem: {data.get('message', 'N/A')}")
            print(f"      Total gerado: {data.get('total_generated', 'N/A')}")
            
        elif response.status_code == 400:
            error = response.json()
            print(f"❌ Erro 400: {error.get('detail', 'Erro desconhecido')}")
            
        elif response.status_code == 405:
            print("❌ Método não permitido - Endpoint pode não existir ou estar mal configurado")
            
        elif response.status_code == 500:
            error = response.json()
            print(f"❌ Erro 500: {error.get('detail', 'Erro interno')}")
            
        else:
            print(f"      Resposta: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - Endpoint pode estar funcionando mas demorou mais que 30s")
        
    except Exception as e:
        print(f"   POST {endpoint}: ERRO - {str(e)}")
    
    # 4. Testar endpoints alternativos
    print("\n4. Testando endpoints alternativos...")
    
    # Testar generate-with-ai
    try:
        # Buscar um tópico para testar
        topics_response = requests.get(f"{API_URL}/topics", headers=headers, timeout=10)
        if topics_response.status_code == 200:
            topics = topics_response.json()
            if topics:
                topic_id = topics[0]['id']
                
                # Testar geração com IA
                ai_data = {
                    "topic_id": topic_id,
                    "quantity": 5,
                    "strategy": "huggingface_only"
                }
                
                response = requests.post(
                    f"{API_URL}/generate-with-ai",
                    headers=headers,
                    json=ai_data,
                    timeout=30
                )
                
                print(f"   POST /generate-with-ai: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Geração com IA funciona! Geradas: {data.get('total_generated', 0)}")
                else:
                    error = response.json() if response.status_code != 500 else {"detail": "Erro interno"}
                    print(f"❌ Erro na geração com IA: {error.get('detail', 'Erro desconhecido')}")
                    
    except Exception as e:
        print(f"   Erro ao testar generate-with-ai: {str(e)}")
    
    # 5. Verificar questões existentes
    print("\n5. Verificando questões existentes...")
    try:
        response = requests.get(f"{API_URL}/questions?limit=5", headers=headers, timeout=10)
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ Questões no banco: {len(questions)} (amostra)")
            
            if questions:
                q = questions[0]
                print(f"   Exemplo: {q.get('disciplina')} - {q.get('topico')}")
            else:
                print("⚠️  Banco de questões vazio - isso pode afetar a geração")
                
        else:
            print(f"❌ Erro ao buscar questões: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar questões: {str(e)}")

if __name__ == "__main__":
    diagnosticar_endpoint()