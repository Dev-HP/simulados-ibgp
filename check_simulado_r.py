#!/usr/bin/env python3
"""
Verifica o simulado 'r' para ver quais questões foram incluídas
"""
import requests

API_URL = "https://simulados-ibgp.onrender.com"

print("🔍 Buscando simulado 'r'...\n")

try:
    # Buscar todos os simulados
    response = requests.get(f"{API_URL}/api/simulados")
    
    if response.status_code == 200:
        simulados = response.json()
        
        # Procurar simulado com nome 'r'
        simulado_r = None
        for sim in simulados:
            if sim.get('nome', '').lower() == 'r':
                simulado_r = sim
                break
        
        if simulado_r:
            print(f"✅ Simulado encontrado: {simulado_r['nome']}")
            print(f"   ID: {simulado_r['id']}")
            print(f"   Disciplina solicitada: {simulado_r.get('disciplina', 'N/A')}")
            print(f"   Total de questões: {simulado_r.get('total_questoes', 0)}")
            
            # Buscar detalhes do simulado
            sim_id = simulado_r['id']
            response2 = requests.get(f"{API_URL}/api/simulados/{sim_id}")
            
            if response2.status_code == 200:
                detalhes = response2.json()
                questoes = detalhes.get('questoes', [])
                
                print(f"\n📊 Análise das questões:")
                print("-" * 60)
                
                from collections import Counter
                disciplinas = Counter([q.get('disciplina', 'N/A') for q in questoes])
                
                for disc, count in disciplinas.items():
                    print(f"   {disc}: {count} questões")
                
                print("\n🔍 Primeiras 5 questões:")
                print("-" * 60)
                for i, q in enumerate(questoes[:5], 1):
                    print(f"   {i}. {q.get('disciplina', 'N/A')} - {q.get('topico', 'N/A')}")
                    print(f"      ID: {q.get('id', 'N/A')}")
                
                # Verificar se há questões de outras disciplinas
                disciplina_esperada = simulado_r.get('disciplina', '')
                if disciplina_esperada:
                    outras = [q for q in questoes if q.get('disciplina') != disciplina_esperada]
                    if outras:
                        print(f"\n⚠️  PROBLEMA ENCONTRADO!")
                        print(f"   Simulado deveria ter apenas: {disciplina_esperada}")
                        print(f"   Mas tem questões de: {list(disciplinas.keys())}")
                        print(f"   Total de questões incorretas: {len(outras)}")
            else:
                print(f"❌ Erro ao buscar detalhes: {response2.status_code}")
        else:
            print("❌ Simulado 'r' não encontrado")
            print("\n📋 Simulados disponíveis:")
            for sim in simulados[:10]:
                print(f"   - {sim.get('nome', 'N/A')} (ID: {sim.get('id')})")
    else:
        print(f"❌ Erro ao buscar simulados: {response.status_code}")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
