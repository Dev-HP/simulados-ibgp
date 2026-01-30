#!/usr/bin/env python3
"""
Script para criar tópicos no banco de dados
FOCO: Concurso Técnico em Informática - IBGP Porto Velho/RO
"""

import os
import sys

# Adicionar o diretório api ao path
api_dir = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_dir)

from database import SessionLocal
from models import Topic

def criar_topicos():
    db = SessionLocal()
    
    # Tópicos focados no concurso de Técnico em Informática
    topicos = [
        # ===== INFORMÁTICA - HARDWARE (5 tópicos) =====
        {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Componentes internos (CPU, RAM, HD, SSD, placa-mãe)"},
        {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Periféricos de entrada e saída"},
        {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Barramentos e interfaces (USB, SATA, PCI)"},
        {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Fontes de alimentação e refrigeração"},
        {"disciplina": "Informática", "topico": "Hardware", "subtopico": "Manutenção preventiva e corretiva"},
        
        # ===== INFORMÁTICA - REDES (6 tópicos) =====
        {"disciplina": "Informática", "topico": "Redes", "subtopico": "Modelo OSI e TCP/IP"},
        {"disciplina": "Informática", "topico": "Redes", "subtopico": "Protocolos (HTTP, HTTPS, FTP, SMTP, DNS, DHCP)"},
        {"disciplina": "Informática", "topico": "Redes", "subtopico": "Endereçamento IP (IPv4 e IPv6)"},
        {"disciplina": "Informática", "topico": "Redes", "subtopico": "Topologias de rede (estrela, anel, barramento)"},
        {"disciplina": "Informática", "topico": "Redes", "subtopico": "Equipamentos (switch, roteador, hub, modem)"},
        {"disciplina": "Informática", "topico": "Redes", "subtopico": "Cabeamento estruturado (par trançado, fibra óptica)"},
        
        # ===== INFORMÁTICA - SISTEMAS OPERACIONAIS (5 tópicos) =====
        {"disciplina": "Informática", "topico": "Windows", "subtopico": "Instalação e configuração (Windows 10/11)"},
        {"disciplina": "Informática", "topico": "Windows", "subtopico": "Gerenciamento de arquivos e pastas"},
        {"disciplina": "Informática", "topico": "Linux", "subtopico": "Comandos básicos (ls, cd, cp, mv, rm, chmod)"},
        {"disciplina": "Informática", "topico": "Linux", "subtopico": "Gerenciamento de usuários e permissões"},
        {"disciplina": "Informática", "topico": "Sistemas Operacionais", "subtopico": "Processos, memória e gerenciamento de recursos"},
        
        # ===== INFORMÁTICA - SEGURANÇA (4 tópicos) =====
        {"disciplina": "Informática", "topico": "Segurança da Informação", "subtopico": "Backup e recuperação de dados"},
        {"disciplina": "Informática", "topico": "Segurança da Informação", "subtopico": "Antivírus e antimalware"},
        {"disciplina": "Informática", "topico": "Segurança da Informação", "subtopico": "Firewall e criptografia"},
        {"disciplina": "Informática", "topico": "Segurança da Informação", "subtopico": "Políticas de segurança e senhas"},
        
        # ===== INFORMÁTICA - APLICATIVOS (4 tópicos) =====
        {"disciplina": "Informática", "topico": "Microsoft Office", "subtopico": "Word (formatação, tabelas, estilos)"},
        {"disciplina": "Informática", "topico": "Microsoft Office", "subtopico": "Excel (fórmulas, funções, gráficos)"},
        {"disciplina": "Informática", "topico": "Microsoft Office", "subtopico": "PowerPoint (apresentações)"},
        {"disciplina": "Informática", "topico": "LibreOffice", "subtopico": "Writer, Calc e Impress"},
        
        # ===== INFORMÁTICA - INTERNET E BANCO DE DADOS (3 tópicos) =====
        {"disciplina": "Informática", "topico": "Internet", "subtopico": "Navegadores (Chrome, Firefox, Edge)"},
        {"disciplina": "Informática", "topico": "Internet", "subtopico": "E-mail e ferramentas de comunicação"},
        {"disciplina": "Informática", "topico": "Banco de Dados", "subtopico": "SQL básico (SELECT, INSERT, UPDATE, DELETE)"},
        
        # ===== PORTUGUÊS (8 tópicos) =====
        {"disciplina": "Português", "topico": "Interpretação de Texto", "subtopico": "Compreensão e análise textual"},
        {"disciplina": "Português", "topico": "Ortografia", "subtopico": "Uso correto das letras"},
        {"disciplina": "Português", "topico": "Acentuação Gráfica", "subtopico": "Regras de acentuação"},
        {"disciplina": "Português", "topico": "Pontuação", "subtopico": "Vírgula, ponto, dois-pontos"},
        {"disciplina": "Português", "topico": "Concordância", "subtopico": "Verbal e nominal"},
        {"disciplina": "Português", "topico": "Regência", "subtopico": "Verbal e nominal"},
        {"disciplina": "Português", "topico": "Crase", "subtopico": "Uso do acento grave"},
        {"disciplina": "Português", "topico": "Redação Oficial", "subtopico": "Ofícios, memorandos e e-mails"},
        
        # ===== MATEMÁTICA (6 tópicos) =====
        {"disciplina": "Matemática", "topico": "Operações Fundamentais", "subtopico": "Adição, subtração, multiplicação, divisão"},
        {"disciplina": "Matemática", "topico": "Frações e Números Decimais", "subtopico": "Operações e conversões"},
        {"disciplina": "Matemática", "topico": "Porcentagem", "subtopico": "Cálculos e aplicações"},
        {"disciplina": "Matemática", "topico": "Regra de Três", "subtopico": "Simples e composta"},
        {"disciplina": "Matemática", "topico": "Equações", "subtopico": "1º e 2º grau"},
        {"disciplina": "Matemática", "topico": "Geometria Básica", "subtopico": "Áreas e perímetros"},
        
        # ===== RACIOCÍNIO LÓGICO (4 tópicos) =====
        {"disciplina": "Raciocínio Lógico", "topico": "Sequências Lógicas", "subtopico": "Numéricas e alfabéticas"},
        {"disciplina": "Raciocínio Lógico", "topico": "Proposições Lógicas", "subtopico": "Verdadeiro e falso"},
        {"disciplina": "Raciocínio Lógico", "topico": "Diagramas de Venn", "subtopico": "Conjuntos e relações"},
        {"disciplina": "Raciocínio Lógico", "topico": "Problemas Lógicos", "subtopico": "Dedução e indução"},
        
        # ===== CONHECIMENTOS GERAIS (3 tópicos) =====
        {"disciplina": "Conhecimentos Gerais", "topico": "Atualidades", "subtopico": "Brasil e mundo"},
        {"disciplina": "Conhecimentos Gerais", "topico": "Rondônia", "subtopico": "Geografia, história e economia"},
        {"disciplina": "Conhecimentos Gerais", "topico": "Porto Velho", "subtopico": "História, cultura e desenvolvimento"},
        
        # ===== LEGISLAÇÃO - RONDÔNIA E SERVIÇO PÚBLICO (6 tópicos) =====
        {"disciplina": "Legislação", "topico": "Constituição Federal", "subtopico": "Direitos e garantias fundamentais"},
        {"disciplina": "Legislação", "topico": "Regime Jurídico Único", "subtopico": "Lei 8.112/90 (Servidores Públicos Federais)"},
        {"disciplina": "Legislação", "topico": "Estatuto dos Servidores de Rondônia", "subtopico": "Lei Complementar Estadual"},
        {"disciplina": "Legislação", "topico": "Ética no Serviço Público", "subtopico": "Deveres e proibições"},
        {"disciplina": "Legislação", "topico": "Lei de Licitações", "subtopico": "Lei 14.133/2021 (Nova Lei de Licitações)"},
        {"disciplina": "Legislação", "topico": "Lei de Acesso à Informação", "subtopico": "Lei 12.527/2011"},
    ]
    
    print(f"\n{'='*60}")
    print(f"CRIANDO TÓPICOS PARA: Técnico em Informática - IBGP Porto Velho/RO")
    print(f"{'='*60}")
    print(f"Total de tópicos: {len(topicos)}\n")
    
    # Contar por disciplina
    from collections import Counter
    disciplinas_count = Counter([t['disciplina'] for t in topicos])
    for disc, count in disciplinas_count.items():
        print(f"  • {disc}: {count} tópicos")
    
    print(f"\n{'='*60}\n")
    
    for i, t in enumerate(topicos, 1):
        # Verificar se já existe
        existing = db.query(Topic).filter(
            Topic.disciplina == t["disciplina"],
            Topic.topico == t["topico"],
            Topic.subtopico == t.get("subtopico")
        ).first()
        
        if not existing:
            topic = Topic(**t)
            db.add(topic)
            print(f"✓ {i:2d}/{len(topicos)} - {t['disciplina']:20s} | {t['topico']}")
        else:
            print(f"⏭ {i:2d}/{len(topicos)} - {t['disciplina']:20s} | {t['topico']} (já existe)")
    
    db.commit()
    print(f"\n{'='*60}")
    print("✓ PROCESSO CONCLUÍDO!")
    print(f"{'='*60}\n")
    db.close()

if __name__ == "__main__":
    criar_topicos()
