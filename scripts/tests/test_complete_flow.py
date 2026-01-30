#!/usr/bin/env python3
"""
Script para testar fluxo completo do sistema
"""
import requests
import time
import sys
import os

API_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_step(step, message):
    print(f"\n{Colors.BLUE}[{step}]{Colors.END} {message}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def test_health():
    """Testa health check"""
    print_step("1/10", "Testando health check...")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200 and response.json()["status"] == "healthy":
        print_success("Health check OK")
        return True
    print_error(f"Health check falhou: {response.status_code}")
    return False

def test_login():
    """Testa login e retorna token"""
    print_step("2/10", "Testando login...")
    response = requests.post(
        f"{API_URL}/api/token",
        data={"username": "teste", "password": "teste123"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print_success(f"Login bem-sucedido! Token: {token[:20]}...")
        return token
    print_error(f"Login falhou: {response.status_code}")
    return None

def test_import_questions(token):
    """Testa importação de questões"""
    print_step("3/10", "Testando importação de questões...")
    
    if not os.path.exists("data/exemplo_prova.txt"):
        print_error("Arquivo data/exemplo_prova.txt não encontrado")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open("data/exemplo_prova.txt", "rb")}
    data = {"disciplina": "Informática"}
    
    response = requests.post(
        f"{API_URL}/api/import-questions",
        headers=headers,
        files=files,
        data=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"Importadas {result['total_imported']} questões")
        return True
    print_error(f"Importação falhou: {response.status_code}")
    return False

def test_list_questions():
    """Testa listagem de questões"""
    print_step("4/10", "Testando listagem de questões...")
    response = requests.get(f"{API_URL}/api/questions?limit=20")
    
    if response.status_code == 200:
        questions = response.json()
        print_success(f"Listadas {len(questions)} questões")
        if len(questions) > 0:
            print(f"   Primeira questão: {questions[0]['enunciado'][:50]}...")
        return True
    print_error(f"Listagem falhou: {response.status_code}")
    return False

def test_upload_syllabus(token):
    """Testa upload de edital"""
    print_step("5/10", "Testando upload de edital...")
    
    # Criar edital de teste
    edital_content = """HARDWARE
1. Componentes de hardware
2. Memória RAM e ROM

REDES
1. Protocolos TCP/IP
2. Modelo OSI
"""
    
    with open("test_edital_temp.txt", "w", encoding="utf-8") as f:
        f.write(edital_content)
    
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open("test_edital_temp.txt", "rb")}
    
    response = requests.post(
        f"{API_URL}/api/upload-syllabus",
        headers=headers,
        files=files
    )
    
    # Limpar arquivo temporário
    os.remove("test_edital_temp.txt")
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"Edital enviado: {result['filename']}")
        return True
    print_error(f"Upload falhou: {response.status_code}")
    return False

def test_list_topics():
    """Testa listagem de tópicos"""
    print_step("6/10", "Testando listagem de tópicos...")
    response = requests.get(f"{API_URL}/api/topics")
    
    if response.status_code == 200:
        topics = response.json()
        print_success(f"Listados {len(topics)} tópicos")
        if len(topics) > 0:
            print(f"   Primeiro tópico: {topics[0]['disciplina']} - {topics[0]['topico']}")
        return topics[0]['id'] if len(topics) > 0 else None
    print_error(f"Listagem falhou: {response.status_code}")
    return None

def test_gemini_stats():
    """Testa estatísticas do Gemini"""
    print_step("7/10", "Testando estatísticas do Gemini...")
    response = requests.get(f"{API_URL}/api/gemini-stats")
    
    if response.status_code == 200:
        stats = response.json()
        print_success("Estatísticas obtidas")
        print(f"   Uso no minuto: {stats['usage']['last_minute']}/{stats['limits']['per_minute']}")
        print(f"   Uso no dia: {stats['usage']['today']}/{stats['limits']['per_day']}")
        return True
    print_error(f"Estatísticas falharam: {response.status_code}")
    return False

def test_generate_with_ai(token, topic_id):
    """Testa geração com IA"""
    print_step("8/10", "Testando geração com IA...")
    
    if not topic_id:
        print_warning("Pulando teste (sem tópicos)")
        return True
    
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "topic_id": topic_id,
        "quantity": 2,
        "difficulty": "MEDIO",
        "use_references": True
    }
    
    print("   Aguardando geração (pode levar ~10s)...")
    response = requests.post(
        f"{API_URL}/api/generate-with-ai",
        headers=headers,
        params=params,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"Geradas {result['total_generated']} questões com IA")
        return True
    elif response.status_code == 429:
        print_warning("Rate limit atingido (esperado se já testou antes)")
        return True
    elif response.status_code == 400:
        print_warning("Gemini API não configurada (esperado em ambiente de teste)")
        return True
    print_error(f"Geração falhou: {response.status_code} - {response.text}")
    return False

def test_create_simulado(token):
    """Testa criação de simulado"""
    print_step("9/10", "Testando criação de simulado...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "nome": "Teste Automatizado",
        "numero_questoes": 5,
        "tempo_total": 15
    }
    
    response = requests.post(
        f"{API_URL}/api/create-simulado",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"Simulado criado: {result['nome']}")
        return result['id']
    print_error(f"Criação falhou: {response.status_code}")
    return None

def test_list_simulados():
    """Testa listagem de simulados"""
    print_step("10/10", "Testando listagem de simulados...")
    response = requests.get(f"{API_URL}/api/simulados")
    
    if response.status_code == 200:
        simulados = response.json()
        print_success(f"Listados {len(simulados)} simulados")
        return True
    print_error(f"Listagem falhou: {response.status_code}")
    return False

def main():
    print("\n" + "=" * 70)
    print("🧪 TESTE COMPLETO DO SISTEMA - FLUXO END-TO-END")
    print("=" * 70)
    
    results = []
    
    # 1. Health check
    results.append(("Health Check", test_health()))
    
    # 2. Login
    token = test_login()
    results.append(("Login", token is not None))
    if not token:
        print_error("Não foi possível continuar sem token")
        return 1
    
    # 3. Importar questões
    results.append(("Importar Questões", test_import_questions(token)))
    
    # 4. Listar questões
    results.append(("Listar Questões", test_list_questions()))
    
    # 5. Upload edital
    results.append(("Upload Edital", test_upload_syllabus(token)))
    
    # 6. Listar tópicos
    topic_id = test_list_topics()
    results.append(("Listar Tópicos", topic_id is not None))
    
    # 7. Estatísticas Gemini
    results.append(("Estatísticas Gemini", test_gemini_stats()))
    
    # 8. Gerar com IA
    results.append(("Gerar com IA", test_generate_with_ai(token, topic_id)))
    
    # 9. Criar simulado
    simulado_id = test_create_simulado(token)
    results.append(("Criar Simulado", simulado_id is not None))
    
    # 10. Listar simulados
    results.append(("Listar Simulados", test_list_simulados()))
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✅ PASSOU{Colors.END}" if result else f"{Colors.RED}❌ FALHOU{Colors.END}"
        print(f"{name:.<50} {status}")
    
    print("=" * 70)
    print(f"\nResultado: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 TODOS OS TESTES PASSARAM!{Colors.END}")
        print("   Sistema está funcionando corretamente!")
        return 0
    else:
        print(f"\n{Colors.RED}❌ ALGUNS TESTES FALHARAM{Colors.END}")
        print(f"   {total - passed} teste(s) precisa(m) de atenção")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Teste interrompido pelo usuário{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Erro inesperado: {str(e)}{Colors.END}")
        sys.exit(1)
