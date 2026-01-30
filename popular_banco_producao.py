#!/usr/bin/env python3
"""
Popular banco de dados em produção
Cria tópicos e questões iniciais
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def popular_banco():
    """Popula o banco de dados com dados iniciais"""
    print("🚀 POPULANDO BANCO DE DADOS EM PRODUÇÃO")
    print("=" * 50)
    
    # 1. Seed database (cria usuário e dados básicos)
    print("📊 Populando dados básicos...")
    try:
        response = requests.post(f"{API_URL}/seed-database", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✅ Dados básicos criados:")
            print(f"   - Usuários: {data.get('data', {}).get('users', 0)}")
            print(f"   - Tópicos: {data.get('data', {}).get('topics', 0)}")
            print(f"   - Questões: {data.get('data', {}).get('questions', 0)}")
        else:
            print(f"⚠️ Seed database: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Erro no seed: {str(e)}")
    
    # 2. Verificar estatísticas
    print("\n📊 Verificando estatísticas...")
    try:
        response = requests.get(f"{API_URL}/estatisticas-banco", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_questoes', 0)
            print(f"✅ Total de questões: {total}")
            
            por_disciplina = data.get('por_disciplina', {})
            if por_disciplina:
                print("📚 Por disciplina:")
                for disciplina, count in por_disciplina.items():
                    print(f"   - {disciplina}: {count} questões")
        else:
            print(f"❌ Erro nas estatísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao verificar estatísticas: {str(e)}")
    
    # 3. Testar geração com IA (se tiver tópicos)
    print("\n🤖 Testando geração com IA...")
    try:
        # Buscar tópicos
        response = requests.get(f"{API_URL}/topics", timeout=10)
        if response.status_code == 200:
            topics = response.json()
            if topics:
                topic = topics[0]
                print(f"📝 Testando com tópico: {topic['topico']} ({topic['disciplina']})")
                
                # Testar geração com HuggingFace
                payload = {
                    "topic_id": topic['id'],
                    "quantity": 1,
                    "difficulty": "MEDIO",
                    "use_references": True,
                    "strategy": "huggingface_only"
                }
                
                response = requests.post(
                    f"{API_URL}/generate-with-ai",
                    params=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    generated = data.get('total_generated', 0)
                    print(f"✅ Geração com IA: {generated} questão gerada")
                else:
                    print(f"⚠️ Geração falhou: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
            else:
                print("⚠️ Nenhum tópico encontrado")
        else:
            print(f"❌ Erro ao buscar tópicos: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no teste de geração: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ POPULAÇÃO DO BANCO CONCLUÍDA!")

if __name__ == "__main__":
    popular_banco()