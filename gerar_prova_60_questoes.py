#!/usr/bin/env python3
"""
GERAR PROVA COMPLETA DE 60 QUESTÕES
Técnico em Informática - IBGP Porto Velho/RO
"""
import sys
import os
import json
import random
from datetime import datetime
sys.path.append('api')

from database import SessionLocal
from models import Question

def gerar_prova_completa():
    """Gera prova completa de 60 questões"""
    print("🎯 GERANDO PROVA COMPLETA - 60 QUESTÕES")
    print("📋 Técnico em Informática - IBGP Porto Velho/RO")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Distribuição da prova conforme edital
        distribuicao = {
            "Informática": 30,
            "Português": 10,
            "Matemática": 8,
            "Raciocínio Lógico": 7,
            "Legislação": 5
        }
        
        prova_questoes = []
        numero_questao = 1
        
        print("📊 SELECIONANDO QUESTÕES POR DISCIPLINA:")
        
        for disciplina, quantidade in distribuicao.items():
            print(f"\n📚 {disciplina}: {quantidade} questões")
            
            # Buscar questões da disciplina
            questoes_disciplina = db.query(Question).filter(
                Question.disciplina == disciplina
            ).all()
            
            if len(questoes_disciplina) < quantidade:
                print(f"⚠️ Apenas {len(questoes_disciplina)} questões disponíveis (precisa {quantidade})")
                questoes_selecionadas = questoes_disciplina
            else:
                # Selecionar aleatoriamente
                questoes_selecionadas = random.sample(questoes_disciplina, quantidade)
                print(f"✅ {quantidade} questões selecionadas aleatoriamente")
            
            # Adicionar à prova
            for questao in questoes_selecionadas:
                prova_questoes.append({
                    "numero": numero_questao,
                    "disciplina": questao.disciplina,
                    "topico": questao.topico,
                    "enunciado": questao.enunciado,
                    "alternativa_a": questao.alternativa_a,
                    "alternativa_b": questao.alternativa_b,
                    "alternativa_c": questao.alternativa_c,
                    "alternativa_d": questao.alternativa_d,
                    "gabarito": questao.gabarito,
                    "explicacao": questao.explicacao_detalhada,
                    "dificuldade": str(questao.dificuldade),
                    "tempo_estimado": questao.estimativa_tempo
                })
                numero_questao += 1
        
        # Embaralhar questões (opcional)
        # random.shuffle(prova_questoes)
        # Renumerar após embaralhar
        # for i, q in enumerate(prova_questoes, 1):
        #     q["numero"] = i
        
        print(f"\n🎯 PROVA GERADA: {len(prova_questoes)} questões")
        
        # Salvar em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"prova_completa_60_questoes_{timestamp}.json"
        
        prova_data = {
            "titulo": "Prova Completa - Técnico em Informática",
            "concurso": "IBGP Porto Velho/RO",
            "data_geracao": datetime.now().isoformat(),
            "total_questoes": len(prova_questoes),
            "distribuicao": distribuicao,
            "tempo_total_estimado": sum(q["tempo_estimado"] for q in prova_questoes),
            "questoes": prova_questoes
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(prova_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Prova salva em: {filename}")
        
        # Salvar também em formato texto legível
        txt_filename = f"prova_completa_60_questoes_{timestamp}.txt"
        
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("🎯 PROVA COMPLETA - TÉCNICO EM INFORMÁTICA\\n")
            f.write("📋 IBGP Porto Velho/RO\\n")
            f.write("=" * 60 + "\\n\\n")
            
            f.write(f"📊 DISTRIBUIÇÃO:\\n")
            for disc, qtd in distribuicao.items():
                f.write(f"• {disc}: {qtd} questões\\n")
            f.write(f"\\n🎯 TOTAL: {len(prova_questoes)} questões\\n")
            f.write(f"⏰ Tempo estimado: {sum(q['tempo_estimado'] for q in prova_questoes)} minutos\\n\\n")
            f.write("=" * 60 + "\\n\\n")
            
            for questao in prova_questoes:
                f.write(f"QUESTÃO {questao['numero']} - {questao['disciplina']} ({questao['topico']})\\n")
                f.write(f"{questao['enunciado']}\\n\\n")
                f.write(f"A) {questao['alternativa_a']}\\n")
                f.write(f"B) {questao['alternativa_b']}\\n")
                f.write(f"C) {questao['alternativa_c']}\\n")
                f.write(f"D) {questao['alternativa_d']}\\n\\n")
                f.write(f"Gabarito: {questao['gabarito']}\\n")
                f.write(f"Explicação: {questao['explicacao']}\\n")
                f.write(f"Dificuldade: {questao['dificuldade']} | Tempo: {questao['tempo_estimado']}min\\n")
                f.write("\\n" + "-" * 60 + "\\n\\n")
        
        print(f"📄 Prova em texto salva em: {txt_filename}")
        
        # Estatísticas da prova
        print("\\n📊 ESTATÍSTICAS DA PROVA:")
        print(f"• Total de questões: {len(prova_questoes)}")
        print(f"• Tempo total estimado: {sum(q['tempo_estimado'] for q in prova_questoes)} minutos")
        
        # Por dificuldade
        dificuldades = {}
        for q in prova_questoes:
            diff = q["dificuldade"]
            dificuldades[diff] = dificuldades.get(diff, 0) + 1
        
        print("\\n📈 POR DIFICULDADE:")
        for diff, count in dificuldades.items():
            print(f"• {diff}: {count} questões")
        
        # Gabarito
        print("\\n📋 GABARITO:")
        gabarito_linha = ""
        for i, q in enumerate(prova_questoes):
            gabarito_linha += f"{q['numero']:2d}-{q['gabarito']} "
            if (i + 1) % 10 == 0:
                print(gabarito_linha)
                gabarito_linha = ""
        if gabarito_linha:
            print(gabarito_linha)
        
        print("\\n🎉 PROVA COMPLETA GERADA COM SUCESSO!")
        print("🚀 Arquivos criados:")
        print(f"   📄 {txt_filename} (formato texto)")
        print(f"   💾 {filename} (formato JSON)")
        
        return prova_questoes
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    prova = gerar_prova_completa()
    
    if prova:
        print("\\n✅ Prova pronta para uso!")
        print("🎯 Pode ser importada no sistema ou usada diretamente")
    else:
        print("\\n❌ Erro na geração da prova")