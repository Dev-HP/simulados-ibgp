#!/usr/bin/env python3
"""
Gera TODAS as questões da prova real do concurso
Câmara de Porto Velho - Técnico em Informática
Seguindo EXATAMENTE o edital
"""

import requests
import time
import json
from datetime import datetime

API_URL = "https://simulados-ibgp.onrender.com"
GEMINI_API_KEY = "AIzaSyBYpSeQqF5k3hyAuLPZw5V-suXwLnGj7XM"

# DISTRIBUIÇÃO EXATA DO EDITAL
# Total: 60 questões
DISTRIBUICAO_EDITAL = {
    "Informática": {
        "total": 30,  # 50% da prova
        "topicos": {
            "Hardware - Componentes internos": 4,
            "Hardware - Periféricos": 2,
            "Redes - Conceitos básicos": 3,
            "Redes - TCP/IP": 3,
            "Redes - Equipamentos": 2,
            "Windows 10/11": 4,
            "Linux básico": 2,
            "Word": 2,
            "Excel": 3,
            "PowerPoint": 1,
            "Segurança da Informação": 2,
            "Internet e E-mail": 2
        }
    },
    "Português": {
        "total": 9,  # 15% da prova
        "topicos": {
            "Interpretação de Texto": 3,
            "Concordância": 2,
            "Regência": 1,
            "Crase": 1,
            "Ortografia": 1,
            "Pontuação": 1
        }
    },
    "Matemática": {
        "total": 6,  # 10% da prova
        "topicos": {
            "Operações básicas": 2,
            "Porcentagem": 2,
            "Regra de Três": 1,
            "Frações": 1
        }
    },
    "Raciocínio Lógico": {
        "total": 4,  # 7% da prova
        "topicos": {
            "Sequências": 2,
            "Proposições": 2
        }
    },
    "Legislação": {
        "total": 7,  # 11% da prova
        "topicos": {
            "Estatuto dos Servidores RO": 3,
            "Ética no Serviço Público": 2,
            "Lei de Licitações": 2
        }
    },
    "Conhecimentos Gerais": {
        "total": 4,  # 7% da prova
        "topicos": {
            "Rondônia": 2,
            "Porto Velho": 1,
            "Atualidades": 1
        }
    }
}

def print_header(msg):
    print(f"\n{'='*70}")
    print(f"  {msg}")
    print('='*70)

def get_token():
    """Faz login"""
    try:
        response = requests.post(
            f"{API_URL}/api/token",
            data={"username": "teste", "password": "teste123"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["access_token"]
    except:
        pass
    return None

def gerar_questoes_topico(token, disciplina, topico, quantidade, dificuldade="MEDIO"):
    """Gera questões para um tópico específico"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "disciplina": disciplina,
            "topico": topico,
            "quantidade": quantidade,
            "dificuldade": dificuldade
        }
        
        response = requests.post(
            f"{API_URL}/api/questions/generate",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            return data.get("questoes_geradas", 0)
        else:
            return 0
            
    except Exception as e:
        return 0

def main():
    print_header("🎯 GERADOR DE PROVA COMPLETA DO CONCURSO")
    print("\n📋 Concurso: Câmara de Porto Velho/RO")
    print("👨‍💻 Cargo: Técnico em Informática")
    print("📝 Total de Questões: 60")
    print(f"🕐 Início: {datetime.now().strftime('%H:%M:%S')}")
    
    # Login
    print_header("1. FAZENDO LOGIN")
    token = get_token()
    
    if not token:
        print("❌ Erro no login. Execute: python inicializar_e_testar.py")
        return 1
    
    print("✅ Login OK")
    
    # Estatísticas
    total_questoes = 0
    total_esperado = 60
    questoes_por_disciplina = {}
    tempo_inicio = time.time()
    
    # Gerar questões por disciplina
    for disciplina, config in DISTRIBUICAO_EDITAL.items():
        print_header(f"📚 {disciplina} ({config['total']} questões)")
        
        questoes_disciplina = 0
        
        for topico, quantidade in config['topicos'].items():
            print(f"\n🎯 {topico}: {quantidade} questões")
            print(f"   Gerando...", end=" ", flush=True)
            
            geradas = gerar_questoes_topico(token, disciplina, topico, quantidade)
            
            if geradas > 0:
                print(f"✅ {geradas} questões criadas")
                questoes_disciplina += geradas
                total_questoes += geradas
            else:
                print(f"❌ Erro ao gerar")
            
            # Aguardar para não exceder rate limit (15 req/min)
            print(f"   Aguardando 5 segundos...")
            time.sleep(5)
        
        questoes_por_disciplina[disciplina] = questoes_disciplina
        
        print(f"\n✅ {disciplina}: {questoes_disciplina}/{config['total']} questões")
    
    # Relatório Final
    tempo_total = time.time() - tempo_inicio
    
    print_header("📊 RELATÓRIO FINAL")
    
    print(f"\n⏱️  Tempo total: {tempo_total/60:.1f} minutos")
    print(f"📝 Questões geradas: {total_questoes}/{total_esperado}")
    print(f"✅ Progresso: {(total_questoes/total_esperado)*100:.1f}%")
    
    print(f"\n📊 Por Disciplina:")
    for disciplina, config in DISTRIBUICAO_EDITAL.items():
        geradas = questoes_por_disciplina.get(disciplina, 0)
        esperado = config['total']
        percentual = (geradas/esperado)*100 if esperado > 0 else 0
        status = "✅" if geradas >= esperado else "⚠️"
        print(f"   {status} {disciplina}: {geradas}/{esperado} ({percentual:.0f}%)")
    
    # Salvar relatório
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "total_geradas": total_questoes,
        "total_esperado": total_esperado,
        "tempo_minutos": tempo_total/60,
        "por_disciplina": questoes_por_disciplina,
        "distribuicao_edital": {k: v['total'] for k, v in DISTRIBUICAO_EDITAL.items()}
    }
    
    with open("relatorio_geracao_prova.json", "w") as f:
        json.dump(relatorio, f, indent=2)
    
    print(f"\n💾 Relatório salvo: relatorio_geracao_prova.json")
    
    if total_questoes >= total_esperado * 0.8:  # 80% ou mais
        print_header("🎉 SUCESSO!")
        print("\n✅ Prova completa gerada com sucesso!")
        print(f"✅ {total_questoes} questões criadas")
        print(f"\n🌐 Acesse: {API_URL}/prova-completa")
        print("🎯 Faça a prova simulada agora!")
        return 0
    else:
        print_header("⚠️  PARCIALMENTE COMPLETO")
        print(f"\n⚠️  Apenas {total_questoes}/{total_esperado} questões geradas")
        print("💡 Execute novamente para completar")
        print("💡 Ou gere manualmente os tópicos faltantes")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
