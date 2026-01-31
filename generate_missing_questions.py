#!/usr/bin/env python3
"""
Script para gerar questões faltantes das disciplinas que não foram geradas
"""
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://simulados-ibgp.onrender.com"

# Disciplinas faltantes e quantidades
FALTANTES = {
    "Matemática": 6,
    "Raciocínio Lógico": 4,
    "Legislação": 7,
    "Conhecimentos Gerais": 4
}

print("🚀 Gerando questões faltantes...\n")

# Primeiro, verificar se os tópicos existem
print("1️⃣ Verificando tópicos...")
try:
    response = requests.get(f"{API_URL}/api/topics")
    if response.status_code == 200:
        topics = response.json()
        topics_by_disc = {}
        for topic in topics:
            disc = topic['disciplina']
            if disc not in topics_by_disc:
                topics_by_disc[disc] = []
            topics_by_disc[disc].append(topic)
        
        print(f"✅ Total de tópicos: {len(topics)}\n")
        
        for disc in FALTANTES.keys():
            count = len(topics_by_disc.get(disc, []))
            print(f"  {disc}: {count} tópicos")
    else:
        print(f"❌ Erro ao buscar tópicos: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    exit(1)

print("\n2️⃣ Gerando questões por disciplina...\n")

total_geradas = 0

for disciplina, quantidade in FALTANTES.items():
    print(f"📝 {disciplina}: gerando {quantidade} questões...")
    
    # Buscar tópicos da disciplina
    disc_topics = topics_by_disc.get(disciplina, [])
    
    if not disc_topics:
        print(f"  ⚠️  Nenhum tópico encontrado para {disciplina}")
        continue
    
    # Distribuir questões entre os tópicos
    questoes_por_topico = quantidade // len(disc_topics)
    resto = quantidade % len(disc_topics)
    
    for i, topic in enumerate(disc_topics):
        qtd = questoes_por_topico + (1 if i < resto else 0)
        
        if qtd == 0:
            continue
        
        print(f"  🔄 {topic['topico']}: gerando {qtd} questões...")
        
        try:
            response = requests.post(
                f"{API_URL}/api/generate-with-ai",
                params={
                    "topic_id": topic['id'],
                    "quantity": qtd,
                    "difficulty": "MEDIO",
                    "use_references": False,
                    "strategy": "huggingface_only"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                geradas = result.get('total_generated', 0)
                total_geradas += geradas
                print(f"    ✅ {geradas} questões geradas")
            else:
                print(f"    ❌ Erro: {response.status_code}")
                print(f"       {response.text[:200]}")
            
            # Aguardar para respeitar rate limit
            time.sleep(3)
            
        except Exception as e:
            print(f"    ❌ Erro: {str(e)}")
    
    print()

print("=" * 50)
print(f"🎉 Total de questões geradas: {total_geradas}")
print("=" * 50)

# Verificar resultado final
print("\n3️⃣ Verificando resultado final...\n")
time.sleep(2)

try:
    response = requests.get(f"{API_URL}/api/questions?limit=200")
    if response.status_code == 200:
        questions = response.json()
        from collections import Counter
        disciplinas = Counter([q['disciplina'] for q in questions])
        
        print("📊 Distribuição final:")
        print("-" * 50)
        for disc, count in sorted(disciplinas.items()):
            print(f"  {disc}: {count} questões")
        
        print(f"\n✅ TOTAL: {len(questions)} questões")
except Exception as e:
    print(f"❌ Erro ao verificar: {str(e)}")
