#!/usr/bin/env python3
"""
Adiciona referências às questões que não têm
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.igpwzskbawbmaftgfkbx:Eliandra2012.@aws-0-us-west-2.pooler.supabase.com:5432/postgres")

print("🔧 Adicionando referências às questões...\n")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Verificar quantas questões não têm referência
    result = conn.execute(text("""
        SELECT COUNT(*) 
        FROM questions 
        WHERE referencia IS NULL OR referencia = ''
    """))
    
    sem_referencia = result.fetchone()[0]
    print(f"📊 Questões sem referência: {sem_referencia}")
    
    if sem_referencia > 0:
        print("\n🔄 Adicionando referências...")
        
        # Adicionar referência baseada na disciplina e tópico
        result = conn.execute(text("""
            UPDATE questions 
            SET referencia = CONCAT('Edital IBGP - ', disciplina, ': ', topico)
            WHERE referencia IS NULL OR referencia = ''
        """))
        conn.commit()
        
        affected = result.rowcount
        print(f"✅ {affected} questões atualizadas")
    else:
        print("✅ Todas as questões já têm referência")
    
    # Verificar resultado final
    result = conn.execute(text("""
        SELECT COUNT(*) 
        FROM questions 
        WHERE referencia IS NOT NULL AND referencia != ''
    """))
    
    com_referencia = result.fetchone()[0]
    
    result = conn.execute(text("SELECT COUNT(*) FROM questions"))
    total = result.fetchone()[0]
    
    print(f"\n📊 Status final:")
    print(f"   Total de questões: {total}")
    print(f"   Com referência: {com_referencia}")
    print(f"   Sem referência: {total - com_referencia}")
    
    if com_referencia == total:
        print("\n✅ Todas as questões têm referência!")
    
    # Mostrar exemplos
    print("\n🔍 Exemplos de referências:")
    print("-" * 60)
    result = conn.execute(text("""
        SELECT id, disciplina, topico, referencia 
        FROM questions 
        LIMIT 5
    """))
    
    for row in result:
        print(f"   ID {row[0]}: {row[1]} - {row[2]}")
        print(f"      Ref: {row[3]}")
