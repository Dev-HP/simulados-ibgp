#!/usr/bin/env python3
"""
Script para popular o banco PostgreSQL do Render remotamente
"""

import requests
import time

# URL da API no Render
API_URL = "https://simulados-ibgp.onrender.com"

# Tópicos para criar
topicos = [
    # Informática (50%)
    {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Componentes internos (CPU, RAM, HD, SSD)", "reference": None},
    {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Periféricos de entrada e saída", "reference": None},
    {"disciplina": "Informática", "topico": "Redes", "subtopico": "Conceitos básicos (LAN, WAN, MAN)", "reference": None},
    {"disciplina": "Informática", "topico": "Redes", "subtopico": "Protocolos TCP/IP", "reference": None},
    {"disciplina": "Informática", "topico": "Redes", "subtopico": "Equipamentos (switch, roteador, hub)", "reference": None},
    {"disciplina": "Informática", "topico": "Sistemas Operacionais", "subtopico": "Windows 10/11", "reference": None},
    {"disciplina": "Informática", "topico": "Sistemas Operacionais", "subtopico": "Linux básico", "reference": None},
    {"disciplina": "Informática", "topico": "Microsoft Office", "subtopico": "Word (formatação, tabelas)", "reference": None},
    {"disciplina": "Informática", "topico": "Microsoft Office", "subtopico": "Excel (fórmulas, funções)", "reference": None},
    {"disciplina": "Informática", "topico": "Microsoft Office", "subtopico": "PowerPoint (apresentações)", "reference": None},
    {"disciplina": "Informática", "topico": "Segurança da Informação", "subtopico": "Conceitos de segurança", "reference": None},
    {"disciplina": "Informática", "topico": "Segurança da Informação", "subtopico": "Backup e recuperação", "reference": None},
    {"disciplina": "Informática", "topico": "Internet", "subtopico": "Navegadores e ferramentas", "reference": None},
    {"disciplina": "Informática", "topico": "Internet", "subtopico": "E-mail e comunicação", "reference": None},
    
    # Português (15%)
    {"disciplina": "Português", "topico": "Interpretação de Texto", "subtopico": "Compreensão e interpretação", "reference": None},
    {"disciplina": "Português", "topico": "Gramática", "subtopico": "Concordância verbal e nominal", "reference": None},
    {"disciplina": "Português", "topico": "Gramática", "subtopico": "Regência verbal e nominal", "reference": None},
    {"disciplina": "Português", "topico": "Gramática", "subtopico": "Crase", "reference": None},
    {"disciplina": "Português", "topico": "Ortografia", "subtopico": "Acentuação gráfica", "reference": None},
    
    # Matemática (10%)
    {"disciplina": "Matemática", "topico": "Aritmética", "subtopico": "Operações básicas", "reference": None},
    {"disciplina": "Matemática", "topico": "Porcentagem", "subtopico": "Cálculos percentuais", "reference": None},
    {"disciplina": "Matemática", "topico": "Regra de Três", "subtopico": "Simples e composta", "reference": None},
    {"disciplina": "Matemática", "topico": "Frações", "subtopico": "Operações com frações", "reference": None},
    
    # Raciocínio Lógico (7%)
    {"disciplina": "Raciocínio Lógico", "topico": "Sequências", "subtopico": "Lógicas e numéricas", "reference": None},
    {"disciplina": "Raciocínio Lógico", "topico": "Proposições", "subtopico": "Lógica proposicional", "reference": None},
    
    # Legislação (11%)
    {"disciplina": "Legislação", "topico": "Estatuto dos Servidores de Rondônia", "subtopico": "Direitos e deveres", "reference": None},
    {"disciplina": "Legislação", "topico": "Ética no Serviço Público", "subtopico": "Princípios éticos", "reference": None},
    {"disciplina": "Legislação", "topico": "Lei de Licitações", "subtopico": "Lei 14.133/2021", "reference": None},
    
    # Conhecimentos Gerais (7%)
    {"disciplina": "Conhecimentos Gerais", "topico": "Rondônia", "subtopico": "Geografia e economia", "reference": None},
    {"disciplina": "Conhecimentos Gerais", "topico": "Porto Velho", "subtopico": "História e atualidades", "reference": None},
]

def criar_topicos():
    """Cria tópicos via API"""
    print("\n" + "="*70)
    print("🚀 POPULANDO BANCO DO RENDER")
    print("="*70)
    print(f"\n📊 Total de tópicos a criar: {len(topicos)}\n")
    
    criados = 0
    erros = 0
    
    for i, topico in enumerate(topicos, 1):
        print(f"[{i}/{len(topicos)}] Criando: {topico['disciplina']} - {topico['topico']}", end=" ")
        
        try:
            response = requests.post(
                f"{API_URL}/api/syllabus/topics",
                json=topico,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅")
                criados += 1
            elif response.status_code == 400 and "already exists" in response.text.lower():
                print("⏭️  (já existe)")
                criados += 1
            else:
                print(f"❌ ({response.status_code})")
                erros += 1
            
            time.sleep(0.5)  # Pequeno delay
            
        except Exception as e:
            print(f"❌ Erro: {str(e)[:30]}")
            erros += 1
    
    print("\n" + "="*70)
    print("🎉 CONCLUÍDO!")
    print("="*70)
    print(f"\n✅ Tópicos criados: {criados}")
    print(f"❌ Erros: {erros}")
    print(f"\n🌐 Acesse: https://simulados-ibgp-1.onrender.com")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        criar_topicos()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro: {str(e)}")
