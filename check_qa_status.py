#!/usr/bin/env python3
"""
Verifica o qa_status das questões de Raciocínio Lógico
"""
import requests

API_URL = "https://simulados-ibgp.onrender.com"

print("🔍 Verificando qa_status das questões...\n")

# Buscar questões de Raciocínio Lógico
response = requests.get(f"{API_URL}/api/questions?disciplina=Raciocínio Lógico&limit=100")

if response.status_code == 200:
    questoes = response.json()
    
    print(f"Total: {len(questoes)} questões de Raciocínio Lógico\n")
    
    print("📊 Status das questões:")
    print("-" * 60)
    
    from collections import Counter
    status_count = Counter([q.get('qa_status', 'N/A') for q in questoes])
    
    for status, count in status_count.items():
        print(f"   {status}: {count} questões")
    
    print("\n🔍 Detalhes de cada questão:")
    print("-" * 60)
    for q in questoes:
        qa_status = q.get('qa_status', 'N/A')
        print(f"   ID {q['id']}: {q['topico']}")
        print(f"      qa_status: {qa_status}")
        print(f"      qa_score: {q.get('qa_score', 'N/A')}")
    
    # Verificar se alguma tem status APPROVED
    approved = [q for q in questoes if q.get('qa_status') == 'APPROVED']
    print(f"\n📋 Questões APPROVED: {len(approved)}")
    
    if len(approved) == 0:
        print("\n❌ PROBLEMA ENCONTRADO!")
        print("   Nenhuma questão de Raciocínio Lógico tem qa_status=APPROVED")
        print("   O SimuladoService só seleciona questões com qa_status=APPROVED")
        print("\n💡 SOLUÇÃO:")
        print("   Precisamos atualizar o qa_status das questões para APPROVED")
else:
    print(f"❌ Erro: {response.status_code}")
