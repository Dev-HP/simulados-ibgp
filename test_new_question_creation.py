#!/usr/bin/env python3
"""
Testa se novas questões são criadas com qa_status=APPROVED e referência
"""
import requests
import time

API_URL = "https://simulados-ibgp.onrender.com"

print("🧪 Testando criação de nova questão...\n")

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

# 2. Contar questões atuais
print("2️⃣ Contando questões atuais...")
response = requests.get(f"{API_URL}/api/questions?limit=1000")
questoes_antes = len(response.json())
print(f"✅ {questoes_antes} questões no banco\n")

# 3. Gerar uma nova questão de teste
print("3️⃣ Gerando nova questão de Matemática...")

# Buscar ID de um tópico de Matemática
response = requests.get(f"{API_URL}/api/topics")
topics = response.json()
topic_matematica = None

for topic in topics:
    if topic['disciplina'] == 'Matemática':
        topic_matematica = topic
        break

if not topic_matematica:
    print("❌ Nenhum tópico de Matemática encontrado")
    exit(1)

print(f"   Tópico: {topic_matematica['topico']}")
print(f"   ID: {topic_matematica['id']}")

# Gerar questão
response = requests.post(
    f"{API_URL}/api/generate-with-ai",
    params={
        "topic_id": topic_matematica['id'],
        "quantity": 1,
        "difficulty": "MEDIO",
        "use_references": False,
        "strategy": "huggingface_only"
    },
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code != 200:
    print(f"❌ Erro ao gerar questão: {response.status_code}")
    print(f"   {response.text}")
    exit(1)

result = response.json()
print(f"✅ Questão gerada: {result.get('total_generated', 0)} questões\n")

# Aguardar um pouco
time.sleep(2)

# 4. Buscar a questão mais recente
print("4️⃣ Verificando questão gerada...")
response = requests.get(f"{API_URL}/api/questions?limit=1000")
questoes_depois = response.json()

if len(questoes_depois) <= questoes_antes:
    print("❌ Nenhuma questão nova foi criada")
    exit(1)

# Pegar a última questão (mais recente)
nova_questao = questoes_depois[-1]

print(f"✅ Nova questão encontrada!")
print(f"   ID: {nova_questao['id']}")
print(f"   Disciplina: {nova_questao['disciplina']}")
print(f"   Tópico: {nova_questao['topico']}")

# 5. Verificar qa_status
print(f"\n5️⃣ Verificando qa_status...")
qa_status = nova_questao.get('qa_status', 'N/A')
qa_score = nova_questao.get('qa_score', 'N/A')

if qa_status == 'APPROVED':
    print(f"   ✅ qa_status: {qa_status}")
    print(f"   ✅ qa_score: {qa_score}")
else:
    print(f"   ❌ qa_status: {qa_status} (deveria ser APPROVED)")
    print(f"   ⚠️  qa_score: {qa_score}")

# 6. Verificar referência
print(f"\n6️⃣ Verificando referência...")
referencia = nova_questao.get('referencia', '')

if referencia and len(referencia) > 0:
    print(f"   ✅ Referência: {referencia}")
else:
    print(f"   ❌ Referência: VAZIA (deveria ter)")

# 7. Testar se pode ser usada em simulado
print(f"\n7️⃣ Testando uso em simulado...")

# Criar simulado de teste
simulado_data = {
    "nome": "Teste Nova Questão",
    "descricao": "Teste para verificar se questão nova pode ser usada",
    "numero_questoes": 1,
    "disciplinas": ["Matemática"],
    "tempo_total": 5,
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
    if simulado['numero_questoes'] > 0:
        print(f"   ✅ Questão pode ser usada em simulados!")
        print(f"   ✅ Simulado criado com {simulado['numero_questoes']} questão(ões)")
    else:
        print(f"   ❌ Simulado criado mas sem questões")
else:
    print(f"   ❌ Erro ao criar simulado: {response.status_code}")

# Resumo final
print("\n" + "=" * 60)
print("📊 RESUMO DO TESTE")
print("=" * 60)

checks = {
    "Questão criada": len(questoes_depois) > questoes_antes,
    "qa_status = APPROVED": qa_status == 'APPROVED' or qa_status == 'approved',
    "qa_score >= 70": qa_score >= 70 if isinstance(qa_score, (int, float)) else False,
    "Tem referência": bool(referencia),
    "Pode ser usada em simulado": simulado['numero_questoes'] > 0 if response.status_code == 200 else False
}

all_ok = all(checks.values())

for check, status in checks.items():
    icon = "✅" if status else "❌"
    print(f"{icon} {check}")

print("=" * 60)

if all_ok:
    print("\n🎉 SUCESSO! Todas as verificações passaram!")
    print("   Novas questões serão criadas corretamente.")
else:
    print("\n⚠️  ATENÇÃO! Algumas verificações falharam.")
    print("   Verifique os logs acima.")
