#!/usr/bin/env python3
"""
Adicionar a questão de Legislação que falta para completar as 60
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Question, Topic, DifficultyLevel, QAStatus

def adicionar_questao():
    """Adiciona a questão de Legislação que falta"""
    print("⚖️ ADICIONANDO QUESTÃO DE LEGISLAÇÃO")
    print("=" * 40)
    
    db = SessionLocal()
    
    try:
        # Buscar tópico de Legislação
        topic = db.query(Topic).filter(
            Topic.disciplina == "Legislação"
        ).first()
        
        if not topic:
            # Criar tópico se não existir
            topic = Topic(
                disciplina="Legislação",
                topico="Direito Administrativo",
                subtopico="Princípios da Administração Pública",
                reference="Constituição Federal Art. 37"
            )
            db.add(topic)
            db.commit()
            db.refresh(topic)
            print("✅ Tópico de Legislação criado")
        
        # Questão adicional de Legislação
        questao_legislacao = {
            "disciplina": "Legislação",
            "topico": "Direito Administrativo",
            "enunciado": "Segundo a Constituição Federal, são princípios da Administração Pública:",
            "alternativa_a": "Legalidade, impessoalidade, moralidade, publicidade e eficiência",
            "alternativa_b": "Apenas legalidade e moralidade",
            "alternativa_c": "Legalidade, pessoalidade e sigilo",
            "alternativa_d": "Moralidade, publicidade e parcialidade",
            "gabarito": "A",
            "explicacao_detalhada": "O Art. 37 da Constituição Federal estabelece que a administração pública direta e indireta obedecerá aos princípios de legalidade, impessoalidade, moralidade, publicidade e eficiência.",
            "dificuldade": DifficultyLevel.MEDIO,
            "estimativa_tempo": 3
        }
        
        # Verificar se já existe
        existing = db.query(Question).filter(
            Question.enunciado == questao_legislacao["enunciado"]
        ).first()
        
        if existing:
            print("⚠️ Questão já existe no banco")
        else:
            # Criar questão
            question = Question(
                topic_id=topic.id,
                disciplina=questao_legislacao["disciplina"],
                topico=questao_legislacao["topico"],
                subtopico=topic.subtopico,
                enunciado=questao_legislacao["enunciado"],
                alternativa_a=questao_legislacao["alternativa_a"],
                alternativa_b=questao_legislacao["alternativa_b"],
                alternativa_c=questao_legislacao["alternativa_c"],
                alternativa_d=questao_legislacao["alternativa_d"],
                gabarito=questao_legislacao["gabarito"],
                explicacao_detalhada=questao_legislacao["explicacao_detalhada"],
                dificuldade=questao_legislacao["dificuldade"],
                estimativa_tempo=questao_legislacao["estimativa_tempo"],
                referencia="Constituição Federal Art. 37",
                keywords=["legislacao", "direito", "administracao"],
                qa_score=0.95,
                qa_status=QAStatus.APPROVED
            )
            
            db.add(question)
            db.commit()
            print("✅ Questão de Legislação adicionada!")
        
        # Verificar total agora
        total_legislacao = db.query(Question).filter(Question.disciplina == "Legislação").count()
        total_geral = db.query(Question).count()
        
        print(f"\n📊 RESULTADO:")
        print(f"• Legislação: {total_legislacao} questões")
        print(f"• Total geral: {total_geral} questões")
        
        if total_legislacao >= 5:
            print("🎉 PRONTO! Agora temos questões suficientes para prova completa!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    adicionar_questao()