#!/usr/bin/env python3
"""
Script para criar usuário de teste no PostgreSQL do Supabase
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import bcrypt

load_dotenv()

# Connection string do Supabase
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.igpwzskbawbmaftgfkbx:Eliandra2012.@aws-0-us-west-2.pooler.supabase.com:5432/postgres")

print(f"🔗 Conectando ao banco: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)

# Criar hash da senha
senha = "teste123".encode('utf-8')
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(senha, salt).decode('utf-8')

print(f"🔐 Hash gerado: {hashed[:30]}...")

# Inserir usuário
with engine.connect() as conn:
    # Verificar se já existe
    result = conn.execute(text("SELECT id FROM users WHERE username = 'teste'"))
    existing = result.fetchone()
    
    if existing:
        print("⚠️  Usuário 'teste' já existe. Atualizando senha...")
        conn.execute(
            text("UPDATE users SET hashed_password = :pwd WHERE username = 'teste'"),
            {"pwd": hashed}
        )
        conn.commit()
        print("✅ Senha atualizada!")
    else:
        print("➕ Criando novo usuário 'teste'...")
        conn.execute(
            text("""
                INSERT INTO users (email, username, hashed_password, full_name, is_active)
                VALUES (:email, :username, :pwd, :name, true)
            """),
            {
                "email": "teste@example.com",
                "username": "teste",
                "pwd": hashed,
                "name": "Usuário Teste"
            }
        )
        conn.commit()
        print("✅ Usuário criado!")

print("\n🎉 Pronto! Agora você pode fazer login com:")
print("   Usuário: teste")
print("   Senha: teste123")
