#!/usr/bin/env python3
"""
Script para gerar questões massivas com IA
FOCO: Concurso Técnico em Informática - Câmara de Porto Velho/RO
"""

import os
import sys
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório api ao path
api_dir = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_dir)

from database import SessionLocal
from models import Topic, Question
from services.gemini_generator import GeminiQuestionGenerator
from services.rate_limiter import RateLimiter

def gerar_questoes_por_disciplina():
    """Gera questões focadas nas disciplinas do concurso"""
    
    db = SessionLocal()
    generator = GeminiQuestionGenerator(db)
    rate_limiter = RateLimiter()
    
    # Configuração de geração por disciplina (AJUSTADO PARA FREE TIER)
    config_geracao = {
        "Informática": {
            "questoes_por_topico": 10,  # Reduzido de 15 para 10
            "dificuldades": ["FACIL", "MEDIO", "DIFICIL"],
            "prioridade": 1
        },
        "Português": {
            "questoes_por_topico": 6,  # Reduzido de 8 para 6
            "dificuldades": ["FACIL", "MEDIO"],
            "prioridade": 2
        },
        "Matemática": {
            "questoes_por_topico": 6,  # Reduzido de 8 para 6
            "dificuldades": ["FACIL", "MEDIO"],
            "prioridade": 3
        },
        "Raciocínio Lógico": {
            "questoes_por_topico": 8,  # Reduzido de 10 para 8
            "dificuldades": ["MEDIO", "DIFICIL"],
            "prioridade": 4
        },
        "Legislação": {
            "questoes_por_topico": 5,  # Reduzido de 6 para 5
            "dificuldades": ["FACIL", "MEDIO"],
            "prioridade": 5
        },
        "Conhecimentos Gerais": {
            "questoes_por_topico": 4,  # Reduzido de 5 para 4
            "dificuldades": ["FACIL"],
            "prioridade": 6
        }
    }
    
    print("\n" + "="*70)
    print("🚀 GERAÇÃO MASSIVA DE QUESTÕES - CÂMARA DE PORTO VELHO")
    print("="*70)
    print("\n📊 Configuração:")
    
    total_estimado = 0
    for disc, config in config_geracao.items():
        topicos_count = db.query(Topic).filter(Topic.disciplina == disc).count()
        estimado = topicos_count * config["questoes_por_topico"]
        total_estimado += estimado
        print(f"  • {disc:25s}: {topicos_count:2d} tópicos × {config['questoes_por_topico']:2d} questões = ~{estimado:3d} questões")
    
    print(f"\n🎯 Total estimado: ~{total_estimado} questões")
    print(f"⏱️  Tempo estimado: ~{total_estimado * 3 // 60} minutos")
    print("\n" + "="*70)
    
    print("\n🔄 Iniciando geração...\n")
    
    total_geradas = 0
    total_erros = 0
    
    # Ordenar disciplinas por prioridade
    disciplinas_ordenadas = sorted(
        config_geracao.items(),
        key=lambda x: x[1]["prioridade"]
    )
    
    for disciplina, config in disciplinas_ordenadas:
        print(f"\n{'='*70}")
        print(f"📚 DISCIPLINA: {disciplina}")
        print(f"{'='*70}\n")
        
        # Buscar tópicos da disciplina
        topicos = db.query(Topic).filter(Topic.disciplina == disciplina).all()
        
        if not topicos:
            print(f"⚠️  Nenhum tópico encontrado para {disciplina}")
            continue
        
        for idx, topico in enumerate(topicos, 1):
            print(f"\n[{idx}/{len(topicos)}] 📖 Tópico: {topico.topico}")
            if topico.subtopico:
                print(f"           Subtópico: {topico.subtopico}")
            
            # Verificar quantas questões já existem
            questoes_existentes = db.query(Question).filter(
                Question.topic_id == topico.id
            ).count()
            
            print(f"           Questões existentes: {questoes_existentes}")
            
            # Gerar questões em diferentes dificuldades
            for dificuldade in config["dificuldades"]:
                quantidade = config["questoes_por_topico"] // len(config["dificuldades"])
                
                print(f"           Gerando {quantidade} questões ({dificuldade})...", end=" ")
                
                try:
                    # Verificar rate limit
                    if not rate_limiter.can_make_request():
                        print("\n⏸️  Rate limit atingido. Aguardando...")
                        time.sleep(60)
                    
                    # Gerar questões com contexto especial para alguns tópicos
                    usar_contexto = False
                    context_type = "pratico"
                    
                    # Definir contexto especial para tópicos específicos
                    if "Porto Velho" in topico.topico:
                        usar_contexto = True
                        context_type = "porto_velho"
                    elif "Rondônia" in topico.topico or "Rondônia" in topico.disciplina:
                        usar_contexto = True
                        context_type = "rondonia"
                    elif disciplina == "Informática" and quantidade <= 3:
                        usar_contexto = True
                        context_type = "trabalho"
                    
                    # Gerar questões
                    if usar_contexto:
                        print(f"[contexto: {context_type}]...", end=" ")
                        questoes_geradas = []
                        for _ in range(quantidade):
                            q = generator.generate_contextual_question(
                                topic=topico,
                                context_type=context_type
                            )
                            if q:
                                questoes_geradas.append(q)
                            time.sleep(2)  # Delay entre questões
                        total_geradas += len(questoes_geradas)
                        print(f"✅ {len(questoes_geradas)} geradas")
                    else:
                        # Buscar questões de referência
                        ref_questions = db.query(Question).filter(
                            Question.disciplina == disciplina
                        ).limit(3).all()
                        
                        ref_dicts = [
                            {
                                'enunciado': q.enunciado,
                                'alternativa_a': q.alternativa_a,
                                'alternativa_b': q.alternativa_b,
                                'alternativa_c': q.alternativa_c,
                                'alternativa_d': q.alternativa_d,
                                'gabarito': q.gabarito,
                                'explicacao_detalhada': q.explicacao_detalhada
                            }
                            for q in ref_questions
                        ]
                        
                        questoes_geradas = generator.generate_questions_with_ai(
                            topic=topico,
                            quantity=quantidade,
                            reference_questions=ref_dicts if ref_dicts else None,
                            difficulty=dificuldade
                        )
                        total_geradas += len(questoes_geradas)
                        print(f"✅ {len(questoes_geradas)} geradas")
                    
                    # Registrar uso da API
                    rate_limiter.record_request()
                    
                    # Pequeno delay para não sobrecarregar (AUMENTADO PARA SEGURANÇA)
                    time.sleep(3)  # Aumentado de 2 para 3 segundos
                    
                except Exception as e:
                    db.rollback()
                    total_erros += 1
                    print(f"❌ Erro: {str(e)[:50]}")
                    
                    # Se for erro de rate limit, aguardar mais
                    if "429" in str(e) or "quota" in str(e).lower():
                        print("⏸️  Aguardando 60 segundos...")
                        time.sleep(60)
        
        # Status da disciplina
        questoes_disciplina = db.query(Question).filter(
            Question.disciplina == disciplina
        ).count()
        print(f"\n✅ {disciplina}: {questoes_disciplina} questões no banco")
    
    print("\n" + "="*70)
    print("🎉 GERAÇÃO CONCLUÍDA!")
    print("="*70)
    print(f"\n📊 Estatísticas:")
    print(f"  • Questões geradas nesta sessão: {total_geradas}")
    print(f"  • Erros: {total_erros}")
    
    # Estatísticas finais por disciplina
    print(f"\n📚 Total no banco por disciplina:")
    for disciplina in config_geracao.keys():
        count = db.query(Question).filter(Question.disciplina == disciplina).count()
        print(f"  • {disciplina:25s}: {count:4d} questões")
    
    total_banco = db.query(Question).count()
    print(f"\n🎯 TOTAL GERAL: {total_banco} questões")
    print("\n" + "="*70 + "\n")
    
    db.close()

if __name__ == "__main__":
    try:
        gerar_questoes_por_disciplina()
    except KeyboardInterrupt:
        print("\n\n⚠️  Geração cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {str(e)}")
        sys.exit(1)
