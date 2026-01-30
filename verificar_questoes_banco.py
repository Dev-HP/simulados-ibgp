#!/usr/bin/env python3
"""
Verificar questões no banco de dados local
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Question, Topic

def verificar_banco():
    """Verifica as questões no banco"""
    print("📊 VERIFICANDO QUESTÕES NO BANCO DE DADOS")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Total de questões
        total = db.query(Question).count()
        print(f"🎯 TOTAL DE QUESTÕES: {total}")
        
        # Por disciplina
        print("\n📚 DISTRIBUIÇÃO POR DISCIPLINA:")
        disciplinas = ["Informática", "Português", "Matemática", "Raciocínio Lógico", "Legislação", "Hardware", "Redes", "Linux"]
        
        for disciplina in disciplinas:
            count = db.query(Question).filter(Question.disciplina == disciplina).count()
            if count > 0:
                print(f"• {disciplina}: {count} questões")
        
        # Por tópico (Informática)
        print("\n💻 INFORMÁTICA - POR TÓPICO:")
        informatica_topicos = db.query(Question.topico).filter(Question.disciplina == "Informática").distinct().all()
        for (topico,) in informatica_topicos:
            count = db.query(Question).filter(
                Question.disciplina == "Informática",
                Question.topico == topico
            ).count()
            print(f"  - {topico}: {count} questões")
        
        # Verificar se temos questões suficientes para uma prova completa
        print("\n🎯 ANÁLISE PARA PROVA COMPLETA (60 questões):")
        
        distribuicao_ideal = {
            "Informática": 30,
            "Português": 10,
            "Matemática": 8,
            "Raciocínio Lógico": 7,
            "Legislação": 5
        }
        
        total_disponivel = 0
        faltam = []
        
        for disciplina, necessario in distribuicao_ideal.items():
            disponivel = db.query(Question).filter(Question.disciplina == disciplina).count()
            total_disponivel += min(disponivel, necessario)
            
            if disponivel >= necessario:
                print(f"✅ {disciplina}: {disponivel} disponível (precisa {necessario})")
            else:
                falta = necessario - disponivel
                print(f"⚠️ {disciplina}: {disponivel} disponível (precisa {necessario}, falta {falta})")
                faltam.append(f"{disciplina}: {falta}")
        
        print(f"\n📊 RESUMO:")
        print(f"• Questões disponíveis para prova: {total_disponivel}/60")
        
        if len(faltam) == 0:
            print("🎉 PRONTO! Temos questões suficientes para gerar prova completa!")
        else:
            print("⚠️ Faltam questões em:")
            for item in faltam:
                print(f"  - {item}")
        
        # Mostrar algumas questões de exemplo
        print("\n📝 EXEMPLOS DE QUESTÕES:")
        exemplos = db.query(Question).limit(3).all()
        for i, q in enumerate(exemplos, 1):
            print(f"\n{i}. {q.disciplina} - {q.topico}")
            print(f"   {q.enunciado[:80]}...")
            print(f"   Gabarito: {q.gabarito}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verificar_banco()