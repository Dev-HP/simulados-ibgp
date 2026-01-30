#!/usr/bin/env python3
"""
Diagnóstico completo do banco de questões
"""

import requests
import json

API_URL = "https://simulados-ibgp.onrender.com"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def get_token():
    """Faz login e retorna token"""
    try:
        response = requests.post(
            f"{API_URL}/api/token",
            data={"username": "teste", "password": "teste123"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    except:
        return None

def check_questions(token):
    """Verifica questões no banco"""
    print_section("VERIFICANDO QUESTÕES NO BANCO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/questions", headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ Total de questões: {len(questions)}")
            
            if len(questions) > 0:
                print(f"\n📋 Primeiras 5 questões:")
                for i, q in enumerate(questions[:5], 1):
                    print(f"\n{i}. ID: {q.get('id')}")
                    print(f"   Disciplina: {q.get('disciplina')}")
                    print(f"   Tópico: {q.get('topico')}")
                    print(f"   Enunciado: {q.get('enunciado', '')[:60]}...")
                    print(f"   Dificuldade: {q.get('dificuldade')}")
                    print(f"   QA Status: {q.get('qa_status')}")
                
                # Agrupar por disciplina
                print(f"\n📊 Por Disciplina:")
                disciplinas = {}
                for q in questions:
                    disc = q.get('disciplina', 'Sem disciplina')
                    disciplinas[disc] = disciplinas.get(disc, 0) + 1
                
                for disc, count in sorted(disciplinas.items()):
                    print(f"   {disc}: {count} questões")
                
                # Agrupar por status QA
                print(f"\n✅ Por Status QA:")
                statuses = {}
                for q in questions:
                    status = q.get('qa_status', 'Sem status')
                    statuses[status] = statuses.get(status, 0) + 1
                
                for status, count in sorted(statuses.items()):
                    print(f"   {status}: {count} questões")
                
                return True
            else:
                print("❌ Nenhuma questão encontrada no banco!")
                return False
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def check_topics(token):
    """Verifica tópicos no banco"""
    print_section("VERIFICANDO TÓPICOS NO BANCO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/topics", headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            topics = response.json()
            print(f"✅ Total de tópicos: {len(topics)}")
            
            # Agrupar por disciplina
            disciplinas = {}
            for t in topics:
                disc = t.get('disciplina', 'Sem disciplina')
                disciplinas[disc] = disciplinas.get(disc, 0) + 1
            
            print(f"\n📊 Por Disciplina:")
            for disc, count in sorted(disciplinas.items()):
                print(f"   {disc}: {count} tópicos")
            
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def check_stats(token):
    """Verifica estatísticas do banco"""
    print_section("VERIFICANDO ESTATÍSTICAS")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/api/estatisticas-banco", headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def suggest_solutions():
    """Sugere soluções"""
    print_section("💡 SOLUÇÕES POSSÍVEIS")
    
    print("""
1. GERAR QUESTÕES COM IA:
   - Acesse: {API_URL}/ai-generator
   - Escolha disciplina e tópico
   - Gere 10-15 questões por vez
   - Aguarde 1 minuto entre gerações

2. IMPORTAR QUESTÕES:
   - Use o endpoint: POST /api/questions/import
   - Ou use o script: python importar_provas.py

3. POPULAR BANCO MANUALMENTE:
   - Acesse: {API_URL}/api/seed-database
   - Cria questões de exemplo

4. VERIFICAR LOGS:
   - Ver logs no Render Dashboard
   - Verificar se há erros de importação
    """.format(API_URL=API_URL))

def main():
    print("\n" + "="*60)
    print("🔍 DIAGNÓSTICO COMPLETO DO BANCO DE QUESTÕES")
    print("="*60)
    print(f"API: {API_URL}")
    
    # Login
    print_section("1. FAZENDO LOGIN")
    token = get_token()
    
    if not token:
        print("❌ Não foi possível fazer login")
        print("Execute: python inicializar_e_testar.py")
        return 1
    
    print("✅ Login OK")
    
    # Verificar questões
    has_questions = check_questions(token)
    
    # Verificar tópicos
    check_topics(token)
    
    # Verificar estatísticas
    check_stats(token)
    
    # Sugerir soluções se não há questões
    if not has_questions:
        suggest_solutions()
        
        print_section("🚀 AÇÃO RECOMENDADA")
        print("""
Para adicionar questões AGORA:

1. Acesse o Gerador IA:
   https://simulados-ibgp.onrender.com/ai-generator

2. Ou use o endpoint seed:
   curl https://simulados-ibgp.onrender.com/api/seed-database

3. Ou gere via script:
   python gerar_questoes_lento.py
        """)
    else:
        print_section("✅ DIAGNÓSTICO COMPLETO")
        print("Sistema tem questões no banco!")
        print("Se não aparecem na interface, pode ser problema de frontend.")
    
    return 0 if has_questions else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
