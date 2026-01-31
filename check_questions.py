#!/usr/bin/env python3
"""
Script para verificar questões geradas no banco PostgreSQL
"""
import os
import requests
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://simulados-ibgp.onrender.com"

print("🔍 Verificando questões geradas...\n")

try:
    # Buscar todas as questões
    response = requests.get(f"{API_URL}/api/questions?limit=200")
    
    if response.status_code == 200:
        questions = response.json()
        
        if not questions:
            print("❌ Nenhuma questão encontrada no banco!")
            print("\n💡 Execute o comando para gerar as questões:")
            print("   POST https://simulados-ibgp.onrender.com/api/generate-complete-exam")
        else:
            print(f"✅ Total de questões: {len(questions)}\n")
            
            # Contar por disciplina
            disciplinas = Counter([q['disciplina'] for q in questions])
            
            print("📊 Distribuição por disciplina:")
            print("-" * 50)
            for disc, count in sorted(disciplinas.items()):
                print(f"  {disc}: {count} questões")
            
            print("\n" + "=" * 50)
            print(f"TOTAL: {len(questions)} / 60 questões ({len(questions)/60*100:.1f}%)")
            print("=" * 50)
            
            # Verificar quais disciplinas faltam
            esperado = {
                "Informática": 30,
                "Português": 9,
                "Matemática": 6,
                "Raciocínio Lógico": 4,
                "Legislação": 7,
                "Conhecimentos Gerais": 4
            }
            
            print("\n📋 Status por disciplina:")
            print("-" * 50)
            for disc, esperado_count in esperado.items():
                atual = disciplinas.get(disc, 0)
                status = "✅" if atual >= esperado_count else "❌"
                print(f"  {status} {disc}: {atual}/{esperado_count}")
            
            # Mostrar últimas 5 questões
            print("\n🔍 Últimas 5 questões geradas:")
            print("-" * 50)
            for q in questions[-5:]:
                print(f"  ID {q['id']}: {q['disciplina']} - {q['topico']}")
    
    else:
        print(f"❌ Erro ao buscar questões: {response.status_code}")
        print(f"   {response.text}")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
