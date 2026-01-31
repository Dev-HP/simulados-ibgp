#!/usr/bin/env python3
"""
Testa criação de simulado apenas com Raciocínio Lógico
"""
import requests

API_URL = "https://simulados-ibgp.onrender.com"

print("🧪 Testando criação de simulado de Raciocínio Lógico...\n")

# 1. Fazer login
print("1️⃣ Fazendo login...")
response = requests.post(
    f"{API_URL}/api/token",
    data={"username": "teste", "password": "teste123"}
)

if response.status_code != 200:
    print(f"❌ Erro no login: {response.status_code}")
    exit(1)

token = response.json()['access_token']
print(f"✅ Login OK\n")

# 2. Verificar questões de Raciocínio Lógico disponíveis
print("2️⃣ Verificando questões de Raciocínio Lógico...")
response = requests.get(
    f"{API_URL}/api/questions?disciplina=Raciocínio Lógico&limit=100"
)

if response.status_code == 200:
    questoes_raciocinio = response.json()
    print(f"✅ {len(questoes_raciocinio)} questões de Raciocínio Lógico disponíveis")
    
    if questoes_raciocinio:
        print("\n📋 Questões disponíveis:")
        for q in questoes_raciocinio:
            print(f"   ID {q['id']}: {q['topico']}")
else:
    print(f"❌ Erro ao buscar questões: {response.status_code}")
    exit(1)

# 3. Criar simulado apenas com Raciocínio Lógico
print("\n3️⃣ Criando simulado de Raciocínio Lógico...")

simulado_data = {
    "nome": "Teste Raciocínio Lógico",
    "descricao": "Simulado apenas com questões de Raciocínio Lógico",
    "numero_questoes": 4,
    "disciplinas": ["Raciocínio Lógico"],  # APENAS Raciocínio Lógico
    "tempo_total": 20,
    "dificuldade_alvo": None,
    "pesos": {},
    "aleatorizacao_por_topico": True
}

response = requests.post(
    f"{API_URL}/api/create-simulado",
    json=simulado_data,
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code == 200:
    simulado = response.json()
    print(f"✅ Simulado criado!")
    print(f"   ID: {simulado['id']}")
    print(f"   Nome: {simulado['nome']}")
    print(f"   Questões: {simulado['numero_questoes']}")
    
    # 4. Verificar as questões do simulado
    print("\n4️⃣ Verificando questões do simulado...")
    sim_id = simulado['id']
    
    response = requests.get(f"{API_URL}/api/simulados/{sim_id}")
    
    if response.status_code == 200:
        detalhes = response.json()
        questoes = detalhes.get('questions', [])
        
        print(f"✅ {len(questoes)} questões no simulado\n")
        
        print("📊 Análise das questões:")
        print("-" * 60)
        
        from collections import Counter
        disciplinas = Counter([q.get('disciplina', 'N/A') for q in questoes])
        
        for disc, count in disciplinas.items():
            status = "✅" if disc == "Raciocínio Lógico" else "❌"
            print(f"   {status} {disc}: {count} questões")
        
        print("\n🔍 Todas as questões:")
        print("-" * 60)
        for i, q in enumerate(questoes, 1):
            disc = q.get('disciplina', 'N/A')
            status = "✅" if disc == "Raciocínio Lógico" else "❌ ERRO"
            print(f"   {i}. {status} {disc} - {q.get('topico', 'N/A')}")
            print(f"      ID: {q.get('id', 'N/A')}")
        
        # Verificar se há erro
        outras_disciplinas = [q for q in questoes if q.get('disciplina') != "Raciocínio Lógico"]
        
        if outras_disciplinas:
            print(f"\n❌ PROBLEMA CONFIRMADO!")
            print(f"   Simulado deveria ter APENAS Raciocínio Lógico")
            print(f"   Mas tem {len(outras_disciplinas)} questões de outras disciplinas:")
            for q in outras_disciplinas:
                print(f"      - ID {q['id']}: {q['disciplina']} - {q['topico']}")
        else:
            print(f"\n✅ TUDO CERTO! Todas as questões são de Raciocínio Lógico")
    else:
        print(f"❌ Erro ao buscar detalhes: {response.status_code}")
else:
    print(f"❌ Erro ao criar simulado: {response.status_code}")
    print(f"   {response.text}")
