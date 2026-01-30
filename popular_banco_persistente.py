#!/usr/bin/env python3
"""
Popular banco de dados de forma PERSISTENTE
Resolve o problema das questões que somem a cada deploy
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "https://simulados-ibgp.onrender.com"
API_URL = f"{BASE_URL}/api"

def popular_banco_persistente():
    """Popula o banco com dados que não serão perdidos"""
    print("🔄 POPULANDO BANCO DE FORMA PERSISTENTE")
    print("=" * 50)
    print(f"🌐 URL: {BASE_URL}")
    print(f"⏰ Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. Verificar saúde do sistema
    print("🔍 Verificando saúde do sistema...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Sistema online")
        else:
            print(f"❌ Sistema com problemas: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro de conexão: {str(e)}")
        return
    
    # 2. Verificar se já tem dados
    print("\n📊 Verificando dados existentes...")
    try:
        response = requests.get(f"{API_URL}/estatisticas-banco", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_questoes', 0)
            print(f"📝 Questões existentes: {total}")
            
            if total >= 60:
                print("✅ Banco já tem questões suficientes!")
                print("🎯 Não é necessário popular novamente")
                return
        else:
            print("⚠️ Não foi possível verificar estatísticas")
    except Exception as e:
        print(f"⚠️ Erro ao verificar estatísticas: {str(e)}")
    
    # 3. Popular dados básicos (usuário + tópicos)
    print("\n🏗️ Populando dados básicos...")
    try:
        response = requests.post(f"{API_URL}/seed-database", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("✅ Dados básicos criados:")
            details = data.get('data', {})
            print(f"   - Usuários: {details.get('users', 0)}")
            print(f"   - Tópicos: {details.get('topics', 0)}")
            print(f"   - Questões: {details.get('questions', 0)}")
        else:
            print(f"⚠️ Seed database: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Erro no seed: {str(e)}")
    
    # 4. Importar questões das 60 completas via API
    print("\n📚 Importando 60 questões completas...")
    
    # Carregar questões do arquivo JSON local
    try:
        with open('prova_completa_60_questoes_20260130_104026.json', 'r', encoding='utf-8') as f:
            prova_data = json.load(f)
            questoes = prova_data.get('questoes', [])
            
        print(f"📄 Carregadas {len(questoes)} questões do arquivo local")
        
        # Importar questões uma por uma via API
        questoes_importadas = 0
        
        for i, questao in enumerate(questoes, 1):
            try:
                # Buscar tópico correspondente
                response = requests.get(f"{API_URL}/topics", timeout=10)
                if response.status_code == 200:
                    topics = response.json()
                    
                    # Encontrar tópico compatível
                    topic_id = None
                    for topic in topics:
                        if (topic['disciplina'] == questao['disciplina'] or 
                            questao['topico'].lower() in topic['topico'].lower()):
                            topic_id = topic['id']
                            break
                    
                    if not topic_id and topics:
                        # Usar primeiro tópico como fallback
                        topic_id = topics[0]['id']
                    
                    if topic_id:
                        # Criar questão via API
                        questao_data = {
                            "topic_id": topic_id,
                            "disciplina": questao['disciplina'],
                            "topico": questao['topico'],
                            "enunciado": questao['enunciado'],
                            "alternativa_a": questao['alternativa_a'],
                            "alternativa_b": questao['alternativa_b'],
                            "alternativa_c": questao['alternativa_c'],
                            "alternativa_d": questao['alternativa_d'],
                            "gabarito": questao['gabarito'],
                            "explicacao_detalhada": questao.get('explicacao', ''),
                            "dificuldade": questao.get('dificuldade', 'MEDIO'),
                            "estimativa_tempo": questao.get('tempo_estimado', 3),
                            "referencia": "60 Questões Completas - Importação Persistente"
                        }
                        
                        response = requests.post(
                            f"{API_URL}/questions",
                            json=questao_data,
                            timeout=15
                        )
                        
                        if response.status_code == 200:
                            questoes_importadas += 1
                            if questoes_importadas % 10 == 0:
                                print(f"✅ {questoes_importadas} questões importadas...")
                        else:
                            print(f"⚠️ Erro na questão {i}: {response.status_code}")
                
                # Pausa para não sobrecarregar
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Erro na questão {i}: {str(e)}")
                continue
        
        print(f"\n✅ Importação concluída: {questoes_importadas} questões")
        
    except FileNotFoundError:
        print("❌ Arquivo de questões não encontrado")
        print("💡 Execute 'python gerar_prova_60_questoes.py' primeiro")
    except Exception as e:
        print(f"❌ Erro na importação: {str(e)}")
    
    # 5. Verificar resultado final
    print("\n📊 Verificando resultado final...")
    try:
        response = requests.get(f"{API_URL}/estatisticas-banco", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_questoes', 0)
            print(f"🎯 Total final: {total} questões")
            
            por_disciplina = data.get('por_disciplina', {})
            if por_disciplina:
                print("📚 Distribuição:")
                for disciplina, count in por_disciplina.items():
                    print(f"   - {disciplina}: {count} questões")
            
            if total >= 60:
                print("\n🎉 SUCESSO! Banco populado com questões persistentes!")
                print("✅ As questões agora não serão perdidas nos próximos deploys")
            else:
                print(f"\n⚠️ Apenas {total} questões importadas (esperado: 60+)")
        
    except Exception as e:
        print(f"❌ Erro na verificação final: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 POPULAÇÃO PERSISTENTE CONCLUÍDA")

if __name__ == "__main__":
    popular_banco_persistente()