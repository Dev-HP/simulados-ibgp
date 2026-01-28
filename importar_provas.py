#!/usr/bin/env python3
"""
Script para importar provas de referência para o banco de dados.
Processa PDFs da pasta data/provas_referencia/
"""

import os
import sys
import requests
from pathlib import Path

# Configuração
API_URL = "http://localhost:8000"

# Detectar o diretório raiz do projeto
SCRIPT_DIR = Path(__file__).parent.absolute()
PROVAS_DIR = SCRIPT_DIR / "data" / "provas_referencia"

def login():
    """Faz login e retorna o token"""
    print("🔐 Fazendo login...")
    
    response = requests.post(
        f"{API_URL}/api/token",
        data={
            "username": "teste",
            "password": "teste123"
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login realizado com sucesso!")
        return token
    else:
        print(f"❌ Erro no login: {response.text}")
        sys.exit(1)

def importar_prova(filepath: Path, token: str):
    """Importa uma prova PDF"""
    print(f"\n📄 Importando: {filepath.name}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(filepath, 'rb') as f:
        files = {
            'file': (filepath.name, f, 'application/pdf')
        }
        data = {
            'source_name': filepath.stem,
            'disciplina': 'Informática'
        }
        
        response = requests.post(
            f"{API_URL}/api/import-questions",
            headers=headers,
            files=files,
            data=data
        )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Importado com sucesso!")
        print(f"   📊 Questões importadas: {result.get('count', 0)}")
        return True
    else:
        print(f"❌ Erro ao importar: {response.text}")
        return False

def main():
    print("=" * 80)
    print("📚 IMPORTADOR DE PROVAS DE REFERÊNCIA")
    print("=" * 80)
    print()
    
    # Verificar se a pasta existe
    if not PROVAS_DIR.exists():
        print(f"❌ Pasta não encontrada: {PROVAS_DIR}")
        print(f"   Crie a pasta e coloque os PDFs das provas lá.")
        sys.exit(1)
    
    # Listar PDFs
    pdfs = list(PROVAS_DIR.glob("*.pdf"))
    
    if not pdfs:
        print(f"❌ Nenhum PDF encontrado em: {PROVAS_DIR}")
        print(f"   Coloque os PDFs das provas nessa pasta.")
        sys.exit(1)
    
    print(f"📁 Encontrados {len(pdfs)} arquivo(s) PDF:")
    for pdf in pdfs:
        print(f"   • {pdf.name}")
    print()
    
    # Verificar se API está rodando
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code != 200:
            raise Exception("API não respondeu")
    except:
        print("❌ API não está rodando!")
        print("   Execute: cd api && uvicorn main:app --reload")
        sys.exit(1)
    
    print("✅ API está rodando")
    print()
    
    # Login
    token = login()
    print()
    
    # Importar cada prova
    success_count = 0
    for pdf in pdfs:
        if importar_prova(pdf, token):
            success_count += 1
    
    print()
    print("=" * 80)
    print(f"✅ Importação concluída!")
    print(f"   📊 {success_count}/{len(pdfs)} arquivo(s) importado(s) com sucesso")
    print("=" * 80)
    print()
    print("💡 Próximos passos:")
    print("   1. Acesse: http://localhost:3000")
    print("   2. Vá em 'Gerador IA'")
    print("   3. Gere novas questões baseadas nas provas importadas")
    print()

if __name__ == "__main__":
    main()
