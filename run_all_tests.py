#!/usr/bin/env python3
"""
Script Master - Executa TODOS os testes automatizados do sistema
"""
import subprocess
import sys
import time
import os
import requests
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}▶ {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def check_prerequisites():
    """Verifica pré-requisitos"""
    print_section("1. VERIFICANDO PRÉ-REQUISITOS")
    
    checks = []
    
    # Python
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Python instalado: {version}")
        checks.append(True)
    except:
        print_error("Python não encontrado")
        checks.append(False)
    
    # Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Node.js instalado: {version}")
        checks.append(True)
    except:
        print_error("Node.js não encontrado")
        checks.append(False)
    
    # Docker
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Docker instalado: {version}")
        checks.append(True)
    except:
        print_warning("Docker não encontrado (opcional)")
        checks.append(True)
    
    # Requests library
    try:
        import requests
        print_success("Biblioteca 'requests' instalada")
        checks.append(True)
    except:
        print_error("Biblioteca 'requests' não encontrada")
        print_info("Execute: pip install requests")
        checks.append(False)
    
    # Arquivos necessários
    required_files = [
        'data/exemplo_prova.txt',
        'test_complete_flow.py',
        'test_rate_limit.py',
        '.env'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print_success(f"Arquivo encontrado: {file}")
            checks.append(True)
        else:
            print_error(f"Arquivo não encontrado: {file}")
            checks.append(False)
    
    return all(checks)

def check_services():
    """Verifica se serviços estão rodando"""
    print_section("2. VERIFICANDO SERVIÇOS")
    
    services = []
    
    # API
    try:
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            print_success("API rodando em http://localhost:8000")
            services.append(('API', True))
        else:
            print_error(f"API respondeu com status {response.status_code}")
            services.append(('API', False))
    except:
        print_error("API não está rodando em http://localhost:8000")
        print_info("Execute: cd api && uvicorn main:app --reload")
        services.append(('API', False))
    
    # Frontend
    try:
        response = requests.get('http://localhost:3000', timeout=2)
        print_success("Frontend rodando em http://localhost:3000")
        services.append(('Frontend', True))
    except:
        print_warning("Frontend não está rodando (opcional para testes de API)")
        print_info("Execute: cd web && npm run dev")
        services.append(('Frontend', False))
    
    # Banco de dados
    try:
        result = subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if 'postgres' in result.stdout:
            print_success("PostgreSQL rodando no Docker")
            services.append(('Database', True))
        else:
            print_warning("PostgreSQL não encontrado no Docker")
            print_info("Execute: docker-compose up -d postgres")
            services.append(('Database', False))
    except:
        print_warning("Não foi possível verificar Docker")
        services.append(('Database', False))
    
    return services

def run_test_script(script_name, description):
    """Executa um script de teste"""
    print_section(f"EXECUTANDO: {description}")
    
    try:
        result = subprocess.run(
            ['python', script_name],
            capture_output=False,
            text=True,
            timeout=300  # 5 minutos
        )
        
        if result.returncode == 0:
            print_success(f"{description} - PASSOU")
            return True
        else:
            print_error(f"{description} - FALHOU (código {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print_error(f"{description} - TIMEOUT (>5min)")
        return False
    except Exception as e:
        print_error(f"{description} - ERRO: {str(e)}")
        return False

def run_api_tests():
    """Executa testes da API via curl"""
    print_section("3. TESTES DA API (CURL)")
    
    API_URL = "http://localhost:8000"
    tests = []
    
    # Test 1: Health Check
    print("Test 1/8: Health Check...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200 and response.json()["status"] == "healthy":
            print_success("Health check OK")
            tests.append(True)
        else:
            print_error(f"Health check falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"Health check erro: {str(e)}")
        tests.append(False)
    
    # Test 2: Docs
    print("Test 2/8: Documentação...")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_success("Documentação acessível")
            tests.append(True)
        else:
            print_error(f"Docs falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"Docs erro: {str(e)}")
        tests.append(False)
    
    # Test 3: Seed user
    print("Test 3/8: Criar usuário de teste...")
    try:
        response = requests.post(f"{API_URL}/api/seed-simple", timeout=10)
        if response.status_code == 200:
            print_success("Usuário criado/existe")
            tests.append(True)
        else:
            print_error(f"Seed falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"Seed erro: {str(e)}")
        tests.append(False)
    
    # Test 4: Login
    print("Test 4/8: Login...")
    try:
        response = requests.post(
            f"{API_URL}/api/token",
            data={"username": "teste", "password": "teste123"},
            timeout=10
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            print_success(f"Login OK - Token: {token[:20]}...")
            tests.append(True)
            
            # Salvar token para próximos testes
            global AUTH_TOKEN
            AUTH_TOKEN = token
        else:
            print_error(f"Login falhou: {response.status_code}")
            tests.append(False)
            AUTH_TOKEN = None
    except Exception as e:
        print_error(f"Login erro: {str(e)}")
        tests.append(False)
        AUTH_TOKEN = None
    
    if not AUTH_TOKEN:
        print_warning("Pulando testes que requerem autenticação")
        return tests
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    # Test 5: List questions
    print("Test 5/8: Listar questões...")
    try:
        response = requests.get(f"{API_URL}/api/questions?limit=10", timeout=10)
        if response.status_code == 200:
            questions = response.json()
            print_success(f"Listadas {len(questions)} questões")
            tests.append(True)
        else:
            print_error(f"List questions falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"List questions erro: {str(e)}")
        tests.append(False)
    
    # Test 6: List topics
    print("Test 6/8: Listar tópicos...")
    try:
        response = requests.get(f"{API_URL}/api/topics", timeout=10)
        if response.status_code == 200:
            topics = response.json()
            print_success(f"Listados {len(topics)} tópicos")
            tests.append(True)
        else:
            print_error(f"List topics falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"List topics erro: {str(e)}")
        tests.append(False)
    
    # Test 7: Gemini stats
    print("Test 7/8: Estatísticas Gemini...")
    try:
        response = requests.get(f"{API_URL}/api/gemini-stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print_success(f"Stats OK - Uso: {stats['usage']['today']}/{stats['limits']['per_day']}")
            tests.append(True)
        else:
            print_error(f"Gemini stats falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"Gemini stats erro: {str(e)}")
        tests.append(False)
    
    # Test 8: List simulados
    print("Test 8/8: Listar simulados...")
    try:
        response = requests.get(f"{API_URL}/api/simulados", timeout=10)
        if response.status_code == 200:
            simulados = response.json()
            print_success(f"Listados {len(simulados)} simulados")
            tests.append(True)
        else:
            print_error(f"List simulados falhou: {response.status_code}")
            tests.append(False)
    except Exception as e:
        print_error(f"List simulados erro: {str(e)}")
        tests.append(False)
    
    return tests

def generate_report(results):
    """Gera relatório final"""
    print_header("RELATÓRIO FINAL DE TESTES")
    
    total_tests = sum(len(tests) for tests in results.values())
    passed_tests = sum(sum(tests) for tests in results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"\n{Colors.BOLD}Resumo Geral:{Colors.END}")
    print(f"  Total de testes: {total_tests}")
    print(f"  {Colors.GREEN}Passaram: {passed_tests}{Colors.END}")
    print(f"  {Colors.RED}Falharam: {failed_tests}{Colors.END}")
    print(f"  Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n{Colors.BOLD}Detalhes por Categoria:{Colors.END}\n")
    
    for category, tests in results.items():
        passed = sum(tests)
        total = len(tests)
        percentage = (passed/total)*100 if total > 0 else 0
        
        status_icon = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
        color = Colors.GREEN if passed == total else Colors.YELLOW if passed > 0 else Colors.RED
        
        print(f"  {status_icon} {category:.<50} {color}{passed}/{total} ({percentage:.0f}%){Colors.END}")
    
    # Salvar relatório em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO DE TESTES AUTOMATIZADOS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total de testes: {total_tests}\n")
        f.write(f"Passaram: {passed_tests}\n")
        f.write(f"Falharam: {failed_tests}\n")
        f.write(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%\n\n")
        f.write("Detalhes por Categoria:\n")
        f.write("-"*80 + "\n")
        for category, tests in results.items():
            passed = sum(tests)
            total = len(tests)
            f.write(f"{category}: {passed}/{total}\n")
    
    print(f"\n{Colors.CYAN}📄 Relatório salvo em: {report_file}{Colors.END}")
    
    return passed_tests == total_tests

def main():
    print_header("🧪 SUITE COMPLETA DE TESTES AUTOMATIZADOS")
    print(f"{Colors.CYAN}Sistema de Simulados IBGP - Teste Completo{Colors.END}\n")
    
    start_time = time.time()
    results = {}
    
    # 1. Pré-requisitos
    if not check_prerequisites():
        print_error("\n❌ Pré-requisitos não atendidos. Corrija os problemas acima.")
        return 1
    
    # 2. Serviços
    services = check_services()
    api_running = any(name == 'API' and status for name, status in services)
    
    if not api_running:
        print_error("\n❌ API não está rodando. Inicie a API antes de continuar.")
        print_info("Execute em outro terminal: cd api && uvicorn main:app --reload")
        return 1
    
    # 3. Testes da API
    api_tests = run_api_tests()
    results['Testes da API (Básicos)'] = api_tests
    
    # 4. Teste Completo (Python)
    print_section("4. TESTE COMPLETO DO FLUXO")
    complete_test_passed = run_test_script('test_complete_flow.py', 'Fluxo End-to-End')
    results['Teste Completo (E2E)'] = [complete_test_passed]
    
    # 5. Teste de Rate Limiting
    print_section("5. TESTE DE RATE LIMITING")
    print_warning("Este teste pode levar ~2 minutos e vai atingir o limite propositalmente")
    user_input = input(f"{Colors.YELLOW}Executar teste de rate limiting? (s/N): {Colors.END}").lower()
    
    if user_input == 's':
        rate_limit_passed = run_test_script('test_rate_limit.py', 'Rate Limiting')
        results['Teste de Rate Limiting'] = [rate_limit_passed]
    else:
        print_info("Teste de rate limiting pulado")
        results['Teste de Rate Limiting'] = []
    
    # 6. Relatório Final
    elapsed_time = time.time() - start_time
    print(f"\n{Colors.CYAN}⏱️  Tempo total: {elapsed_time:.1f} segundos{Colors.END}")
    
    all_passed = generate_report(results)
    
    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODOS OS TESTES PASSARAM!{Colors.END}")
        print(f"{Colors.GREEN}   Sistema está funcionando perfeitamente!{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ALGUNS TESTES FALHARAM{Colors.END}")
        print(f"{Colors.RED}   Revise os erros acima e corrija os problemas.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Testes interrompidos pelo usuário{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Erro inesperado: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
