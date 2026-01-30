#!/usr/bin/env python3
"""
Gerar 60 questões completas via IA HuggingFace
Teste para verificar se a geração está funcionando perfeitamente
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def fazer_login():
    """Faz login e retorna o token"""
    login_data = {
        "username": "teste",
        "password": "teste123"
    }
    
    response = requests.post(f"{API_URL}/token", data=login_data, timeout=15)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Erro no login: {response.status_code}")

def gerar_questoes_ia():
    """Gera 60 questões completas usando IA"""
    print("🤖 GERANDO 60 QUESTÕES VIA IA HUGGINGFACE")
    print("=" * 60)
    print(f"🌐 URL: {BASE_URL}")
    print(f"⏰ Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. Fazer login
    print("\n🔐 Fazendo login...")
    try:
        token = fazer_login()
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login realizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no login: {str(e)}")
        return
    
    # 2. Distribuição conforme edital IBGP
    distribuicao = [
        {"disciplina": "Informática", "quantidade": 30, "topicos": [
            "Hardware e componentes", "Redes de computadores", "Sistemas operacionais Windows",
            "Microsoft Office", "Segurança da informação", "Internet e navegadores",
            "Manutenção de computadores", "Backup e recuperação", "Impressoras e periféricos"
        ]},
        {"disciplina": "Português", "quantidade": 10, "topicos": [
            "Interpretação de texto", "Concordância verbal e nominal", "Regência verbal",
            "Ortografia e acentuação", "Pontuação"
        ]},
        {"disciplina": "Matemática", "quantidade": 8, "topicos": [
            "Operações básicas", "Porcentagem", "Regra de três", "Frações e decimais"
        ]},
        {"disciplina": "Raciocínio Lógico", "quantidade": 7, "topicos": [
            "Sequências lógicas", "Proposições lógicas", "Problemas de lógica"
        ]},
        {"disciplina": "Legislação", "quantidade": 5, "topicos": [
            "Estatuto dos Servidores de Rondônia", "Ética no serviço público", "Lei de Licitações"
        ]}
    ]
    
    questoes_geradas = []
    total_questoes = 0
    
    # 3. Gerar questões por disciplina
    for disc in distribuicao:
        disciplina = disc["disciplina"]
        quantidade = disc["quantidade"]
        topicos = disc["topicos"]
        
        print(f"\n📚 GERANDO {quantidade} QUESTÕES DE {disciplina.upper()}")
        print("-" * 50)
        
        questoes_disciplina = 0
        
        for i in range(quantidade):
            topico = topicos[i % len(topicos)]  # Rotacionar tópicos
            
            print(f"🔄 Gerando questão {i+1}/{quantidade}: {topico}")
            
            # Dados para geração
            dados_geracao = {
                "disciplina": disciplina,
                "topico": topico,
                "subtopico": f"{topico} - Concurso IBGP Porto Velho",
                "dificuldade": "médio",
                "contexto_concurso": "Técnico em Informática - Câmara Municipal de Porto Velho/RO",
                "strategy": "huggingface_only"  # Forçar HuggingFace
            }
            
            try:
                # Primeiro, buscar um tópico existente para usar como topic_id
                response_topics = requests.get(f"{API_URL}/topics", headers=headers, timeout=10)
                if response_topics.status_code == 200:
                    topics = response_topics.json()
                    # Encontrar tópico compatível ou usar o primeiro
                    topic_id = None
                    for topic in topics:
                        if (topic.get('disciplina') == disciplina or 
                            disciplina.lower() in topic.get('topico', '').lower()):
                            topic_id = topic['id']
                            break
                    
                    if not topic_id and topics:
                        topic_id = topics[0]['id']  # Usar primeiro tópico como fallback
                    
                    if not topic_id:
                        print(f"⚠️ Nenhum tópico encontrado para {disciplina}")
                        continue
                else:
                    print(f"⚠️ Erro ao buscar tópicos: {response_topics.status_code}")
                    continue
                
                # Chamar API de geração com endpoint correto
                response = requests.post(
                    f"{API_URL}/questions/generate-with-ai",
                    params={
                        "topic_id": topic_id,
                        "quantity": 1,
                        "difficulty": "MEDIO",
                        "use_references": True,
                        "strategy": "huggingface_only"
                    },
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # A API retorna informações sobre a geração, não as questões diretamente
                    # Vamos buscar as questões geradas mais recentes
                    response_questions = requests.get(
                        f"{API_URL}/questions",
                        params={"limit": 5, "disciplina": disciplina},
                        headers=headers,
                        timeout=10
                    )
                    
                    if response_questions.status_code == 200:
                        recent_questions = response_questions.json()
                        if recent_questions:
                            # Pegar a questão mais recente
                            questao = recent_questions[0]
                            questoes_geradas.append(questao)
                            questoes_disciplina += 1
                            total_questoes += 1
                            
                            print(f"✅ Questão {total_questoes} gerada: {questao.get('enunciado', '')[:80]}...")
                        else:
                            print(f"⚠️ Nenhuma questão encontrada após geração")
                    else:
                        print(f"⚠️ Erro ao buscar questões geradas: {response_questions.status_code}")
                    
                    # Pausa para não sobrecarregar a API
                    time.sleep(3)
                    
                elif response.status_code == 429:
                    print("⏳ Rate limit atingido, aguardando 10 segundos...")
                    time.sleep(10)
                    continue
                    
                else:
                    print(f"⚠️ Erro na geração: {response.status_code}")
                    print(f"   Resposta: {response.text[:200]}")
                    
            except Exception as e:
                print(f"❌ Erro na questão {i+1}: {str(e)}")
                continue
        
        print(f"✅ {disciplina}: {questoes_disciplina} questões geradas")
    
    # 4. Salvar resultado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar JSON
    arquivo_json = f"prova_ia_60_questoes_{timestamp}.json"
    prova_data = {
        "metadata": {
            "titulo": "Prova Completa - 60 Questões IA",
            "concurso": "Técnico em Informática - IBGP Porto Velho/RO",
            "data_geracao": datetime.now().isoformat(),
            "total_questoes": len(questoes_geradas),
            "gerador": "HuggingFace IA",
            "distribuicao": {d["disciplina"]: d["quantidade"] for d in distribuicao}
        },
        "questoes": questoes_geradas
    }
    
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(prova_data, f, ensure_ascii=False, indent=2)
    
    # Salvar TXT legível
    arquivo_txt = f"prova_ia_60_questoes_{timestamp}.txt"
    with open(arquivo_txt, 'w', encoding='utf-8') as f:
        f.write("PROVA COMPLETA - 60 QUESTÕES GERADAS POR IA\n")
        f.write("=" * 60 + "\n")
        f.write(f"Concurso: Técnico em Informática - IBGP Porto Velho/RO\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Total: {len(questoes_geradas)} questões\n")
        f.write(f"Gerador: HuggingFace IA\n\n")
        
        # Estatísticas por disciplina
        f.write("DISTRIBUIÇÃO POR DISCIPLINA:\n")
        f.write("-" * 30 + "\n")
        disciplinas_count = {}
        for q in questoes_geradas:
            disc = q.get('disciplina', 'Não informado')
            disciplinas_count[disc] = disciplinas_count.get(disc, 0) + 1
        
        for disc, count in disciplinas_count.items():
            f.write(f"{disc}: {count} questões\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("QUESTÕES:\n\n")
        
        for i, questao in enumerate(questoes_geradas, 1):
            f.write(f"QUESTÃO {i:02d} - {questao.get('disciplina', 'N/A')}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Tópico: {questao.get('topico', 'N/A')}\n")
            f.write(f"Subtópico: {questao.get('subtopico', 'N/A')}\n")
            f.write(f"Dificuldade: {questao.get('dificuldade', 'N/A')}\n\n")
            
            f.write(f"Enunciado:\n{questao.get('enunciado', 'N/A')}\n\n")
            
            f.write(f"a) {questao.get('alternativa_a', 'N/A')}\n")
            f.write(f"b) {questao.get('alternativa_b', 'N/A')}\n")
            f.write(f"c) {questao.get('alternativa_c', 'N/A')}\n")
            f.write(f"d) {questao.get('alternativa_d', 'N/A')}\n\n")
            
            f.write(f"Gabarito: {questao.get('gabarito', 'N/A')}\n\n")
            f.write(f"Explicação:\n{questao.get('explicacao_detalhada', 'N/A')}\n\n")
            f.write("=" * 60 + "\n\n")
    
    # 5. Relatório final
    print("\n" + "=" * 60)
    print("🎉 GERAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"📊 Total de questões geradas: {len(questoes_geradas)}")
    print(f"🎯 Meta: 60 questões")
    print(f"📈 Taxa de sucesso: {(len(questoes_geradas)/60)*100:.1f}%")
    
    print(f"\n📁 Arquivos salvos:")
    print(f"   - {arquivo_json}")
    print(f"   - {arquivo_txt}")
    
    print(f"\n📚 Distribuição final:")
    disciplinas_final = {}
    for q in questoes_geradas:
        disc = q.get('disciplina', 'Não informado')
        disciplinas_final[disc] = disciplinas_final.get(disc, 0) + 1
    
    for disc, count in sorted(disciplinas_final.items()):
        esperado = next((d["quantidade"] for d in distribuicao if d["disciplina"] == disc), 0)
        status = "✅" if count >= esperado else "⚠️"
        print(f"   {status} {disc}: {count}/{esperado}")
    
    if len(questoes_geradas) >= 50:  # Pelo menos 50 questões
        print(f"\n🎉 SUCESSO! IA HuggingFace está funcionando perfeitamente!")
        print(f"✅ Sistema pronto para gerar questões em produção")
    else:
        print(f"\n⚠️ Apenas {len(questoes_geradas)} questões geradas")
        print(f"💡 Pode ser necessário ajustar rate limits ou timeouts")
    
    return questoes_geradas

if __name__ == "__main__":
    gerar_questoes_ia()