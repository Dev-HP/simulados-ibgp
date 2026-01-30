#!/usr/bin/env python3
"""
Testar endpoint corrigido para usar HuggingFace
"""
import requests
import json

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def testar_endpoint_huggingface():
    """Testa o endpoint corrigido para HuggingFace"""
    print("🤗 TESTANDO ENDPOINT COM HUGGINGFACE")
    print("=" * 40)
    
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
    
    # 2. Verificar status dos geradores
    print("\n2. Verificando status dos geradores...")
    try:
        response = requests.get(f"{API_URL}/ai-generators-status", headers=headers, timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✅ Status obtido")
            
            hf_status = status.get('generators', {}).get('huggingface', {})
            hf_available = hf_status.get('available', False)
            hf_api_key = hf_status.get('api_key_configured', False)
            
            print(f"   HuggingFace disponível: {hf_available}")
            print(f"   HuggingFace API key: {hf_api_key}")
            
            if not hf_available or not hf_api_key:
                print("⚠️  AVISO: HuggingFace pode não estar configurado corretamente")
                
        else:
            print(f"❌ Erro ao verificar status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    # 3. Testar geração com IA (pequena)
    print("\n3. Testando geração pequena com HuggingFace...")
    try:
        # Buscar tópicos
        topics_response = requests.get(f"{API_URL}/topics", headers=headers, timeout=10)
        if topics_response.status_code == 200:
            topics = topics_response.json()
            if topics:
                topic_id = topics[0]['id']
                print(f"   Usando tópico: {topics[0]['disciplina']} - {topics[0]['topico']}")
                
                # Testar geração de 2 questões
                ai_data = {
                    "topic_id": topic_id,
                    "quantity": 2,
                    "strategy": "huggingface_only"
                }
                
                response = requests.post(
                    f"{API_URL}/generate-with-ai",
                    headers=headers,
                    json=ai_data,
                    timeout=60
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Geração pequena OK! Geradas: {data.get('total_generated', 0)}")
                    print(f"   Estratégia: {data.get('strategy_used', 'N/A')}")
                else:
                    error = response.json() if response.status_code != 500 else {"detail": "Erro interno"}
                    print(f"❌ Erro na geração: {error.get('detail', 'Erro desconhecido')}")
                    
        else:
            print("❌ Não foi possível buscar tópicos")
            
    except Exception as e:
        print(f"❌ Erro no teste pequeno: {str(e)}")
    
    # 4. Testar endpoint de 60 questões
    print("\n4. Testando endpoint de 60 questões...")
    try:
        print("   ⚠️  AVISO: Isso pode demorar 10-15 minutos!")
        print("   Iniciando geração...")
        
        response = requests.post(
            f"{API_URL}/generate-complete-exam",
            headers=headers,
            timeout=1200  # 20 minutos de timeout
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("🎉 SUCESSO! Endpoint de 60 questões funcionou!")
            print(f"   Mensagem: {data.get('message', 'N/A')}")
            print(f"   Total gerado: {data.get('total_generated', 'N/A')}")
            print(f"   Esperado: {data.get('expected', 'N/A')}")
            print(f"   Percentual: {data.get('percentage', 'N/A')}%")
            print(f"   Estratégia: {data.get('strategy_used', 'N/A')}")
            
            if 'report' in data:
                print("\n📊 Relatório por disciplina:")
                for disciplina, topicos in data['report'].items():
                    if isinstance(topicos, dict):
                        total_disciplina = sum(topicos.values())
                        print(f"   {disciplina}: {total_disciplina} questões")
                        for topico, qtd in topicos.items():
                            if qtd > 0:
                                print(f"     - {topico}: {qtd}")
                    else:
                        print(f"   {disciplina}: {topicos} questões")
                        
        elif response.status_code == 400:
            error = response.json()
            print(f"❌ Erro 400: {error.get('detail', 'Erro desconhecido')}")
            
        elif response.status_code == 500:
            error = response.json()
            print(f"❌ Erro 500: {error.get('detail', 'Erro interno')}")
            
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - A geração pode estar funcionando mas demorou mais que 20 min")
        print("   Isso é normal para 60 questões. Verifique o banco depois.")
        
    except Exception as e:
        print(f"❌ Erro no teste de 60 questões: {str(e)}")

if __name__ == "__main__":
    testar_endpoint_huggingface()