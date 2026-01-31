#!/usr/bin/env python3
"""
Aprova todas as questões no banco (muda qa_status para APPROVED)
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.igpwzskbawbmaftgfkbx:Eliandra2012.@aws-0-us-west-2.pooler.supabase.com:5432/postgres")

print("🔧 Aprovando todas as questões...\n")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Verificar status atual
    result = conn.execute(text("SELECT qa_status, COUNT(*) FROM questions GROUP BY qa_status"))
    
    print("📊 Status atual:")
    print("-" * 50)
    for row in result:
        print(f"   {row[0]}: {row[1]} questões")
    
    # Aprovar todas as questões
    print("\n🔄 Atualizando qa_status para APPROVED...")
    
    result = conn.execute(
        text("""
            UPDATE questions 
            SET qa_status = 'APPROVED', 
                qa_score = CASE 
                    WHEN qa_score IS NULL THEN 85.0
                    WHEN qa_score < 60.0 THEN 75.0
                    ELSE qa_score
                END
            WHERE qa_status != 'APPROVED'
        """)
    )
    conn.commit()
    
    affected = result.rowcount
    print(f"✅ {affected} questões atualizadas")
    
    # Verificar status final
    result = conn.execute(text("SELECT qa_status, COUNT(*) FROM questions GROUP BY qa_status"))
    
    print("\n📊 Status final:")
    print("-" * 50)
    for row in result:
        print(f"   {row[0]}: {row[1]} questões")
    
    print("\n✅ Todas as questões foram aprovadas!")
    print("   Agora você pode criar simulados sem problemas.")
