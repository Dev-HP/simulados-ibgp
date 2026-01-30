#!/usr/bin/env python3
"""
Salvar as 60 questões completas no banco de dados local
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Question, Topic, DifficultyLevel, QAStatus
from questoes_60_completas import questoes_60

def salvar_questoes():
    """Salva as 60 questões no banco de dados"""
    print("🚀 SALVANDO 60 QUESTÕES NO BANCO DE DADOS")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        questoes_salvas = 0
        questoes_puladas = 0
        
        # Primeiro, vamos criar os tópicos necessários se não existirem
        topicos_necessarios = [
            ("Informática", "Hardware"),
            ("Informática", "Redes"),
            ("Informática", "Windows"),
            ("Informática", "Linux"),
            ("Informática", "Sistemas Operacionais"),
            ("Informática", "Segurança da Informação"),
            ("Informática", "Microsoft Office"),
            ("Informática", "LibreOffice"),
            ("Português", "Interpretação de Texto"),
            ("Português", "Ortografia"),
            ("Português", "Acentuação Gráfica"),
            ("Português", "Pontuação"),
            ("Português", "Concordância"),
            ("Português", "Regência"),
            ("Português", "Crase"),
            ("Português", "Redação Oficial"),
            ("Matemática", "Operações Fundamentais"),
            ("Matemática", "Frações"),
            ("Matemática", "Porcentagem"),
            ("Matemática", "Regra de Três"),
            ("Matemática", "Equações"),
            ("Matemática", "Geometria Básica"),
            ("Matemática", "Números Decimais"),
            ("Raciocínio Lógico", "Sequências Lógicas"),
            ("Raciocínio Lógico", "Proposições Lógicas"),
            ("Raciocínio Lógico", "Problemas Lógicos"),
            ("Raciocínio Lógico", "Diagramas de Venn"),
            ("Legislação", "Constituição Federal"),
            ("Legislação", "Lei 8.112/90"),
            ("Legislação", "Ética no Serviço Público"),
            ("Legislação", "Lei de Licitações"),
            ("Legislação", "Lei de Acesso à Informação")
        ]
        
        print("📚 Criando tópicos necessários...")
        topicos_criados = 0
        
        for disciplina, topico in topicos_necessarios:
            existing = db.query(Topic).filter(
                Topic.disciplina == disciplina,
                Topic.topico == topico
            ).first()
            
            if not existing:
                new_topic = Topic(
                    disciplina=disciplina,
                    topico=topico,
                    subtopico=f"Questões de {topico}",
                    reference="Criação automática para 60 questões"
                )
                db.add(new_topic)
                topicos_criados += 1
        
        db.commit()
        print(f"✅ {topicos_criados} tópicos criados")
        
        # Agora salvar as questões
        print("\n📝 Salvando questões...")
        
        for i, q_data in enumerate(questoes_60, 1):
            try:
                # Buscar tópico correspondente
                topic = db.query(Topic).filter(
                    Topic.disciplina == q_data["disciplina"],
                    Topic.topico == q_data["topico"]
                ).first()
                
                if not topic:
                    print(f"⚠️ Tópico não encontrado: {q_data['disciplina']} - {q_data['topico']}")
                    questoes_puladas += 1
                    continue
                
                # Verificar se questão já existe (evitar duplicatas)
                existing_question = db.query(Question).filter(
                    Question.enunciado == q_data["enunciado"]
                ).first()
                
                if existing_question:
                    print(f"⚠️ Questão {i} já existe (pulando)")
                    questoes_puladas += 1
                    continue
                
                # Converter dificuldade
                dificuldade_map = {
                    "FACIL": DifficultyLevel.FACIL,
                    "MEDIO": DifficultyLevel.MEDIO,
                    "DIFICIL": DifficultyLevel.DIFICIL
                }
                
                # Criar questão
                question = Question(
                    topic_id=topic.id,
                    disciplina=q_data["disciplina"],
                    topico=q_data["topico"],
                    subtopico=topic.subtopico,
                    enunciado=q_data["enunciado"],
                    alternativa_a=q_data["alternativa_a"],
                    alternativa_b=q_data["alternativa_b"],
                    alternativa_c=q_data["alternativa_c"],
                    alternativa_d=q_data["alternativa_d"],
                    gabarito=q_data["gabarito"],
                    explicacao_detalhada=q_data["explicacao_detalhada"],
                    dificuldade=dificuldade_map.get(q_data["dificuldade"], DifficultyLevel.MEDIO),
                    estimativa_tempo=q_data["estimativa_tempo"],
                    referencia="60 Questões Completas - Técnico Informática IBGP",
                    fonte="Criação Manual Baseada em Análise do Projeto",
                    keywords=[q_data["disciplina"].lower(), q_data["topico"].lower()],
                    qa_score=0.95,
                    qa_status=QAStatus.APPROVED
                )
                
                db.add(question)
                questoes_salvas += 1
                
                if questoes_salvas % 10 == 0:
                    print(f"✅ {questoes_salvas} questões salvas...")
                
            except Exception as e:
                print(f"❌ Erro na questão {i}: {str(e)}")
                questoes_puladas += 1
        
        db.commit()
        
        print("\n" + "=" * 50)
        print("📊 RESULTADO FINAL:")
        print(f"✅ Questões salvas: {questoes_salvas}")
        print(f"⚠️ Questões puladas: {questoes_puladas}")
        print(f"🎯 Total processadas: {len(questoes_60)}")
        
        # Verificar distribuição no banco
        print("\n📚 DISTRIBUIÇÃO NO BANCO:")
        for disciplina in ["Informática", "Português", "Matemática", "Raciocínio Lógico", "Legislação"]:
            count = db.query(Question).filter(Question.disciplina == disciplina).count()
            print(f"• {disciplina}: {count} questões")
        
        total_banco = db.query(Question).count()
        print(f"\n🎯 TOTAL NO BANCO: {total_banco} questões")
        
        if questoes_salvas > 0:
            print("\n🎉 SUCESSO! As questões foram salvas no banco de dados!")
            print("🚀 Agora você pode usar o sistema para gerar provas completas!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    salvar_questoes()