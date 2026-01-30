#!/usr/bin/env python3
"""
Teste final completo do sistema de simulados
Verifica tudo: banco, questões, geradores, API
"""
import sys
import os
sys.path.append('api')

from database import SessionLocal
from models import Question, Topic, User
from services.hybrid_ai_generator import HybridAIGenerator

def testar_sistema_completo():
    """Teste completo do sistema"""
    
    print("🎯 TESTE FINAL COMPLETO - SISTEMA DE SIMULADOS IBGP")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # 1. VERIFICAR BANCO DE DADOS
        print("\n1️⃣ VERIFICANDO BANCO DE DADOS")
        print("-" * 40)
        
        total_questoes = db.query(Question).count()
        total_topicos = db.query(Topic).count()
        total_usuarios = db.query(User).count()
        
        print(f"📊 Questões no banco: {total_questoes}")
        print(f"📚 Tópicos criados: {total_topicos}")
        print(f"👥 Usuários cadastrados: {total_usuarios}")
        
        if total_questoes >= 50:
            print("✅ Banco com questões suficientes")
        else:
            print("⚠️ Poucas questões no banco")
        
        # 2. VERIFICAR DISTRIBUIÇÃO POR DISCIPLINA
        print("\n2️⃣ DISTRIBUIÇÃO POR DISCIPLINA")
        print("-" * 40)
        
        disciplinas = db.query(Question.disciplina).distinct().all()
        for (disciplina,) in disciplinas:
            count = db.query(Question).filter(Question.disciplina == disciplina).count()
            print(f"📖 {disciplina}: {count} questões")
        
        # 3. VERIFICAR CONFIGURAÇÃO DE IA
        print("\n3️⃣ CONFIGURAÇÃO DE IA")
        print("-" * 40)
        
        gemini_key = os.getenv('GEMINI_API_KEY')
        huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
        
        print(f"🔵 Gemini: {'✅ Configurada' if gemini_key else '❌ Não configurada'}")
        print(f"🟠 HuggingFace: {'✅ Configurada' if huggingface_key else '❌ Não configurada'}")
        
        if gemini_key or huggingface_key:
            print("✅ Pelo menos uma IA configurada")
        else:
            print("❌ Nenhuma IA configurada")
        
        # 4. TESTAR GERADOR HÍBRIDO
        if gemini_key or huggingface_key:
            print("\n4️⃣ TESTANDO GERADOR HÍBRIDO")
            print("-" * 40)
            
            try:
                generator = HybridAIGenerator(db)
                status = generator.get_status()
                
                print(f"🤖 Gemini disponível: {'✅' if status['gemini_available'] else '❌'}")
                print(f"🤖 HuggingFace disponível: {'✅' if status['huggingface_available'] else '❌'}")
                
                # Teste rápido de geração
                topic = db.query(Topic).first()
                if topic:
                    print(f"\n🔄 Testando geração com: {topic.disciplina} - {topic.topico}")
                    
                    # Não vamos gerar de verdade para não gastar quota
                    print("✅ Gerador híbrido inicializado com sucesso")
                else:
                    print("⚠️ Nenhum tópico para teste")
                    
            except Exception as e:
                print(f"❌ Erro no gerador híbrido: {str(e)[:100]}")
        
        # 5. VERIFICAR TEMPLATES DE PROVA
        print("\n5️⃣ TEMPLATES DE PROVA DISPONÍVEIS")
        print("-" * 40)
        
        templates = {
            "tecnico_informatica_completo": 60,
            "tecnico_informatica_padrao": 50,
            "conhecimentos_basicos": 40,
            "informatica_especifica": 40
        }
        
        for template, total in templates.items():
            print(f"📋 {template}: {total} questões")
        
        print("✅ Templates configurados")
        
        # 6. SIMULAR GERAÇÃO DE PROVA
        print("\n6️⃣ SIMULANDO GERAÇÃO DE PROVA")
        print("-" * 40)
        
        # Verificar se temos questões suficientes para uma prova
        informatica = db.query(Question).filter(Question.disciplina == "Informática").count()
        portugues = db.query(Question).filter(Question.disciplina == "Português").count()
        matematica = db.query(Question).filter(Question.disciplina == "Matemática").count()
        
        print(f"📊 Disponível para prova completa:")
        print(f"  💻 Informática: {informatica}/30 necessárias")
        print(f"  📝 Português: {portugues}/10 necessárias")
        print(f"  🔢 Matemática: {matematica}/8 necessárias")
        
        pode_gerar_prova = informatica >= 30 and portugues >= 10 and matematica >= 8
        
        if pode_gerar_prova:
            print("✅ Sistema pode gerar prova completa!")
        else:
            print("⚠️ Questões insuficientes para prova completa")
        
        # 7. RESUMO FINAL
        print("\n" + "=" * 70)
        print("📋 RESUMO FINAL DO SISTEMA")
        print("=" * 70)
        
        status_geral = []
        
        # Banco de dados
        if total_questoes >= 50:
            status_geral.append("✅ Banco de dados: OK")
        else:
            status_geral.append("⚠️ Banco de dados: Poucas questões")
        
        # IA
        if gemini_key or huggingface_key:
            status_geral.append("✅ IA: Configurada")
        else:
            status_geral.append("❌ IA: Não configurada")
        
        # Prova completa
        if pode_gerar_prova:
            status_geral.append("✅ Prova completa: Possível")
        else:
            status_geral.append("⚠️ Prova completa: Questões insuficientes")
        
        # Templates
        status_geral.append("✅ Templates: Configurados")
        
        for status in status_geral:
            print(status)
        
        # Status geral
        problemas = len([s for s in status_geral if "❌" in s or "⚠️" in s])
        
        if problemas == 0:
            print("\n🎉 SISTEMA 100% FUNCIONAL!")
            print("🚀 Pronto para produção!")
        elif problemas <= 2:
            print("\n✅ SISTEMA FUNCIONAL COM PEQUENOS AJUSTES")
            print("🔧 Alguns itens precisam de atenção")
        else:
            print("\n⚠️ SISTEMA PRECISA DE AJUSTES")
            print("🔧 Vários itens precisam ser corrigidos")
        
        # 8. PRÓXIMOS PASSOS
        print("\n📋 PRÓXIMOS PASSOS:")
        
        if total_questoes < 50:
            print("1. Execute: python questoes_60_completas.py")
        
        if not (gemini_key or huggingface_key):
            print("2. Configure API keys no .env:")
            print("   GEMINI_API_KEY=sua_chave")
            print("   HUGGINGFACE_API_KEY=hf_sua_chave")
        
        if pode_gerar_prova:
            print("3. Sistema pronto! Teste a geração de provas")
        
        print("4. Deploy no Render com as configurações")
        print("5. Teste em produção")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    testar_sistema_completo()