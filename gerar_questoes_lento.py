#!/usr/bin/env python3
"""
Script LENTO para gerar questões com IA
Respeita limites do Gemini FREE (15 req/min)
"""

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

api_dir = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_dir)

from database import SessionLocal
from models import Topic, Question
from services.gemini_generator import GeminiQuestionGenerator

def gerar_lento():
    """Gera questões DEVAGAR para não bater no rate limit"""
    
    db = SessionLocal()
    generator = GeminiQuestionGenerator(db)
    
    # Configuração CONSERVADORA
    QUESTOES_POR_LOTE = 5  # Apenas 5 por vez
    DELAY_ENTRE_LOTES = 30  # 30 segundos entre lotes
    
    print("\n" + "="*70)
    print("🐢 GERAÇÃO LENTA - Respeitando Rate Limit do Gemini FREE")
    print("="*70)
    print(f"\n⚙️  Configuração:")
    print(f"  • {QUESTOES_POR_LOTE} questões por lote")
    print(f"  • {DELAY_ENTRE_LOTES} segundos entre lotes")
    print(f"  • ~12 questões por minuto")
    print(f"  • Pode cancelar a qualquer momento (Ctrl+C)")
    
    # Prioridade de tópicos
    prioridades = {
        "Informática": 1,
        "Português": 2,
        "Matemática": 3,
        "Raciocínio Lógico": 4,
        "Legislação": 5,
        "Conhecimentos Gerais": 6
    }
    
    # Buscar todos os tópicos ordenados por prioridade
    topicos = db.query(Topic).all()
    topicos_ordenados = sorted(
        topicos,
        key=lambda t: (prioridades.get(t.disciplina, 99), t.topico)
    )
    
    print(f"\n📚 Total de tópicos: {len(topicos_ordenados)}")
    
    total_geradas = 0
    lote_numero = 0
    
    print("\n" + "="*70)
    print("🚀 Iniciando geração...")
    print("="*70 + "\n")
    
    for topico in topicos_ordenados:
        # Verificar quantas questões já existem
        existentes = db.query(Question).filter(Question.topic_id == topico.id).count()
        
        # Se já tem 10+, pular
        if existentes >= 10:
            print(f"⏭️  {topico.disciplina} - {topico.topico}: {existentes} questões (pulando)")
            continue
        
        # Calcular quantas faltam
        faltam = 10 - existentes
        gerar = min(faltam, QUESTOES_POR_LOTE)
        
        print(f"\n📖 {topico.disciplina} - {topico.topico}")
        print(f"   Existentes: {existentes} | Faltam: {faltam} | Gerando: {gerar}")
        
        try:
            # Gerar questões
            for i in range(gerar):
                print(f"   [{i+1}/{gerar}] Gerando...", end=" ", flush=True)
                
                questao = generator.generate_contextual_question(
                    topic=topico,
                    context_type="pratico"
                )
                
                if questao:
                    total_geradas += 1
                    print("✅")
                else:
                    print("❌")
                
                # Delay entre questões
                time.sleep(5)
            
            lote_numero += 1
            
            # Delay entre lotes
            if lote_numero % 3 == 0:  # A cada 3 lotes (15 questões)
                print(f"\n⏸️  Pausa de {DELAY_ENTRE_LOTES}s (total geradas: {total_geradas})...")
                time.sleep(DELAY_ENTRE_LOTES)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Cancelado pelo usuário")
            break
        except Exception as e:
            print(f"\n❌ Erro: {str(e)[:50]}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("⏸️  Rate limit! Aguardando 60 segundos...")
                time.sleep(60)
    
    # Estatísticas finais
    print("\n" + "="*70)
    print("🎉 GERAÇÃO CONCLUÍDA")
    print("="*70)
    print(f"\n📊 Questões geradas nesta sessão: {total_geradas}")
    
    print(f"\n📚 Total no banco por disciplina:")
    for disc in prioridades.keys():
        count = db.query(Question).filter(Question.disciplina == disc).count()
        print(f"  • {disc:25s}: {count:4d} questões")
    
    total = db.query(Question).count()
    print(f"\n🎯 TOTAL GERAL: {total} questões")
    print("\n" + "="*70 + "\n")
    
    db.close()

if __name__ == "__main__":
    try:
        gerar_lento()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Erro: {str(e)}")
        sys.exit(1)
