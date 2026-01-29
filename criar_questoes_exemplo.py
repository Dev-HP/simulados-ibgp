#!/usr/bin/env python3
"""
Cria questões de exemplo diretamente via API
"""

import requests
import json

API_URL = "https://simulados-ibgp.onrender.com"

# Login
print("🔐 Fazendo login...")
token_response = requests.post(
    f"{API_URL}/api/token",
    data={"username": "teste", "password": "teste123"},
    timeout=10
)

if token_response.status_code != 200:
    print("❌ Erro no login")
    exit(1)

token = token_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

print("✅ Login OK\n")

# Buscar tópicos
print("📚 Buscando tópicos...")
topics_response = requests.get(f"{API_URL}/api/topics", headers=headers, timeout=10)
topics = topics_response.json()

print(f"✅ {len(topics)} tópicos encontrados\n")

# Questões de exemplo
questoes_exemplo = [
    {
        "disciplina": "Informática",
        "topico": "Hardware",
        "subtopico": "Componentes internos",
        "enunciado": "Qual componente é responsável pelo processamento de dados no computador?",
        "alternativa_a": "CPU (Processador)",
        "alternativa_b": "Memória RAM",
        "alternativa_c": "HD (Disco Rígido)",
        "alternativa_d": "Placa de Vídeo",
        "gabarito": "A",
        "explicacao_detalhada": "A CPU (Central Processing Unit) é o componente responsável pelo processamento de dados e execução de instruções no computador.",
        "dificuldade": "FACIL",
        "estimativa_tempo": 2,
        "keywords": ["hardware", "cpu", "processador"]
    },
    {
        "disciplina": "Informática",
        "topico": "Redes",
        "subtopico": "TCP/IP",
        "enunciado": "Qual protocolo é usado para transferência de páginas web?",
        "alternativa_a": "FTP",
        "alternativa_b": "HTTP",
        "alternativa_c": "SMTP",
        "alternativa_d": "POP3",
        "gabarito": "B",
        "explicacao_detalhada": "HTTP (HyperText Transfer Protocol) é o protocolo usado para transferência de páginas web na internet.",
        "dificuldade": "FACIL",
        "estimativa_tempo": 2,
        "keywords": ["redes", "http", "protocolo"]
    },
    {
        "disciplina": "Informática",
        "topico": "Windows",
        "subtopico": "Windows 10/11",
        "enunciado": "Qual atalho abre o Gerenciador de Tarefas no Windows?",
        "alternativa_a": "Ctrl + Alt + Del",
        "alternativa_b": "Ctrl + Shift + Esc",
        "alternativa_c": "Alt + F4",
        "alternativa_d": "Windows + R",
        "gabarito": "B",
        "explicacao_detalhada": "Ctrl + Shift + Esc abre diretamente o Gerenciador de Tarefas no Windows. Ctrl + Alt + Del abre um menu com várias opções.",
        "dificuldade": "MEDIO",
        "estimativa_tempo": 2,
        "keywords": ["windows", "atalho", "gerenciador"]
    },
    {
        "disciplina": "Informática",
        "topico": "Office",
        "subtopico": "Word e Excel",
        "enunciado": "No Excel, qual função soma valores de um intervalo?",
        "alternativa_a": "=SOMA(A1:A10)",
        "alternativa_b": "=TOTAL(A1:A10)",
        "alternativa_c": "=ADD(A1:A10)",
        "alternativa_d": "=SOMAR(A1:A10)",
        "gabarito": "A",
        "explicacao_detalhada": "A função =SOMA() é usada no Excel para somar valores de um intervalo de células.",
        "dificuldade": "FACIL",
        "estimativa_tempo": 2,
        "keywords": ["excel", "função", "soma"]
    },
    {
        "disciplina": "Português",
        "topico": "Interpretação",
        "subtopico": "Compreensão de texto",
        "enunciado": "Em 'O menino correu rapidamente', qual é o advérbio?",
        "alternativa_a": "menino",
        "alternativa_b": "correu",
        "alternativa_c": "rapidamente",
        "alternativa_d": "O",
        "gabarito": "C",
        "explicacao_detalhada": "'Rapidamente' é um advérbio de modo que modifica o verbo 'correu', indicando como a ação foi realizada.",
        "dificuldade": "FACIL",
        "estimativa_tempo": 2,
        "keywords": ["português", "advérbio", "gramática"]
    },
    {
        "disciplina": "Matemática",
        "topico": "Aritmética",
        "subtopico": "Operações básicas",
        "enunciado": "Quanto é 15% de 200?",
        "alternativa_a": "15",
        "alternativa_b": "20",
        "alternativa_c": "30",
        "alternativa_d": "35",
        "gabarito": "C",
        "explicacao_detalhada": "15% de 200 = 0,15 × 200 = 30",
        "dificuldade": "FACIL",
        "estimativa_tempo": 2,
        "keywords": ["matemática", "porcentagem", "cálculo"]
    },
    {
        "disciplina": "Raciocínio Lógico",
        "topico": "Sequências",
        "subtopico": "Lógicas e numéricas",
        "enunciado": "Qual número completa a sequência: 2, 4, 8, 16, __?",
        "alternativa_a": "20",
        "alternativa_b": "24",
        "alternativa_c": "32",
        "alternativa_d": "64",
        "gabarito": "C",
        "explicacao_detalhada": "A sequência multiplica por 2 a cada termo: 2×2=4, 4×2=8, 8×2=16, 16×2=32",
        "dificuldade": "MEDIO",
        "estimativa_tempo": 3,
        "keywords": ["lógica", "sequência", "padrão"]
    },
    {
        "disciplina": "Legislação",
        "topico": "Estatuto RO",
        "subtopico": "Servidores",
        "enunciado": "Qual é o regime jurídico dos servidores públicos de Rondônia?",
        "alternativa_a": "CLT",
        "alternativa_b": "Estatutário",
        "alternativa_c": "Temporário",
        "alternativa_d": "Terceirizado",
        "gabarito": "B",
        "explicacao_detalhada": "Os servidores públicos de Rondônia são regidos pelo regime estatutário, conforme o Estatuto dos Servidores Públicos do Estado.",
        "dificuldade": "MEDIO",
        "estimativa_tempo": 2,
        "keywords": ["legislação", "estatuto", "servidores"]
    },
    {
        "disciplina": "Conhecimentos Gerais",
        "topico": "Porto Velho",
        "subtopico": "História",
        "enunciado": "Porto Velho é a capital de qual estado?",
        "alternativa_a": "Acre",
        "alternativa_b": "Amazonas",
        "alternativa_c": "Rondônia",
        "alternativa_d": "Roraima",
        "gabarito": "C",
        "explicacao_detalhada": "Porto Velho é a capital do estado de Rondônia, localizada na região Norte do Brasil.",
        "dificuldade": "FACIL",
        "estimativa_tempo": 1,
        "keywords": ["geografia", "porto velho", "capital"]
    },
    {
        "disciplina": "Informática",
        "topico": "Segurança",
        "subtopico": "Conceitos",
        "enunciado": "O que é um firewall?",
        "alternativa_a": "Um antivírus",
        "alternativa_b": "Um sistema de proteção de rede",
        "alternativa_c": "Um navegador web",
        "alternativa_d": "Um sistema operacional",
        "gabarito": "B",
        "explicacao_detalhada": "Firewall é um sistema de segurança que monitora e controla o tráfego de rede, bloqueando acessos não autorizados.",
        "dificuldade": "MEDIO",
        "estimativa_tempo": 2,
        "keywords": ["segurança", "firewall", "rede"]
    }
]

print(f"📝 Criando {len(questoes_exemplo)} questões...\n")

criadas = 0
erros = 0

for i, questao in enumerate(questoes_exemplo, 1):
    try:
        # Buscar topic_id correspondente
        topic = next((t for t in topics if t['disciplina'] == questao['disciplina'] and t['topico'] == questao['topico']), None)
        
        if topic:
            questao['topic_id'] = topic['id']
            
            response = requests.post(
                f"{API_URL}/api/questions",
                headers=headers,
                json=questao,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                criadas += 1
                print(f"✅ [{i}/{len(questoes_exemplo)}] {questao['disciplina']} - {questao['topico']}")
            else:
                erros += 1
                print(f"❌ [{i}/{len(questoes_exemplo)}] Erro: {response.status_code}")
        else:
            erros += 1
            print(f"⚠️  [{i}/{len(questoes_exemplo)}] Tópico não encontrado: {questao['disciplina']} - {questao['topico']}")
            
    except Exception as e:
        erros += 1
        print(f"❌ [{i}/{len(questoes_exemplo)}] Exceção: {str(e)}")

print(f"\n{'='*60}")
print(f"✅ Questões criadas: {criadas}")
print(f"❌ Erros: {erros}")
print(f"{'='*60}\n")

# Verificar total
print("🔍 Verificando total no banco...")
questions_response = requests.get(f"{API_URL}/api/questions", headers=headers, timeout=10)
if questions_response.status_code == 200:
    total = len(questions_response.json())
    print(f"✅ Total de questões no banco: {total}\n")
    
    if total > 0:
        print("🎉 SUCESSO! Questões criadas e disponíveis!")
        print(f"\n🌐 Acesse: {API_URL}/ai-generator")
        print("💡 Agora você pode gerar mais questões com IA!")
    else:
        print("⚠️  Nenhuma questão no banco ainda")
else:
    print(f"❌ Erro ao verificar: {questions_response.status_code}")
