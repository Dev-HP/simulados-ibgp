#!/usr/bin/env python3
"""
Teste direto do endpoint de geração de questões
"""
import requests
import json
import os
from datetime import datetime

def main():
    print("🔍 TESTANDO ENDPOINT DIRETO")
    print("=" * 50)
    
    base_url = "https://simulados-ibgp.onrender.com"
    
    # 1. Login
    print("🔐 Fazendo login...")
    login_data = {
        "username": "teste",
        "password": "teste123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/token", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login OK")
        else:
            print(f"❌ Login falhou: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Listar tópicos
    print("\n📚 Listando tópicos...")
    try:
        response = requests.get(f"{base_url}/api/topics", headers=headers)
        if response.status_code == 200:
            topics = response.json()
            print(f"✅ {len(topics)} tópicos encontrados")
            if topics:
                topic_id = topics[0]["id"]
                topic_name = topics[0]["topico"]
                print(f"📝 Usando tópico: {topic_name} (ID: {topic_id})")
            else:
                print("❌ Nenhum tópico encontrado")
                return
        else:
            print(f"❌ Erro ao listar tópicos: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro ao listar tópicos: {e}")
        return
    
    # 3. Testar endpoint de geração correto
    print(f"\n🤖 Testando geração com tópico {topic_id}...")
    
    # O endpoint correto é POST com parâmetros de query
    print(f"\n🔄 Testando POST /api/questions/generate-with-ai com query params")
    
    try:
        # Parâmetros como query string
        params = {
            "topic_id": topic_id,
            "quantity": 1,
            "difficulty": "MEDIO",
            "use_references": True,
            "strategy": "huggingface_only"
        }
        
        print(f"  Parâmetros: {params}")
        response = requests.post(f"{base_url}/api/questions/generate-with-ai", 
                               params=params, headers=headers)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Sucesso!")
            print(f"  📊 Questões geradas: {result.get('total_generated', 0)}")
            print(f"  🎯 Tópico: {result.get('topic', 'N/A')}")
            print(f"  🤖 Estratégia: {result.get('strategy_used', 'N/A')}")
        else:
            print(f"  ❌ Erro: {response.text[:500]}")
            
    except Exception as e:
        print(f"  ❌ Erro na requisição: {e}")
    
    # Testar também sem parâmetros opcionais
    print(f"\n🔄 Testando com parâmetros mínimos")
    try:
        params = {"topic_id": topic_id, "quantity": 1}
        print(f"  Parâmetros: {params}")
        response = requests.post(f"{base_url}/api/questions/generate-with-ai", 
                               params=params, headers=headers)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ Sucesso!")
            print(f"  📊 Questões geradas: {result.get('total_generated', 0)}")
        else:
            print(f"  ❌ Erro: {response.text[:500]}")
            
    except Exception as e:
        print(f"  ❌ Erro na requisição: {e}")
    
    # 4. Verificar documentação da API
    print(f"\n📖 Verificando documentação...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ Documentação disponível em /docs")
        else:
            print(f"❌ Documentação não disponível: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar docs: {e}")

if __name__ == "__main__":
    main()