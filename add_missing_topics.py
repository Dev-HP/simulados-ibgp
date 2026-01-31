#!/usr/bin/env python3
"""
Script para adicionar tópicos faltantes no banco PostgreSQL do Supabase
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.igpwzskbawbmaftgfkbx:Eliandra2012.@aws-0-us-west-2.pooler.supabase.com:5432/postgres")

print(f"🔗 Conectando ao banco...")

engine = create_engine(DATABASE_URL)

# Tópicos faltantes
topicos_faltantes = [
    ("Matemática", "Aritmética", "Operações básicas"),
    ("Matemática", "Porcentagem", "Cálculos percentuais"),
    ("Matemática", "Regra de Três", "Simples e composta"),
    ("Matemática", "Frações", "Operações com frações"),
    ("Raciocínio Lógico", "Sequências", "Lógicas e numéricas"),
    ("Raciocínio Lógico", "Proposições", "Lógica proposicional"),
    ("Legislação", "Estatuto dos Servidores de Rondônia", "Direitos e deveres"),
    ("Legislação", "Ética no Serviço Público", "Princípios éticos"),
    ("Legislação", "Lei de Licitações", "Lei 14.133/2021"),
    ("Conhecimentos Gerais", "Rondônia", "Geografia e economia"),
    ("Conhecimentos Gerais", "Porto Velho", "História e atualidades"),
    ("Conhecimentos Gerais", "Atualidades", "Brasil e região Norte"),
]

with engine.connect() as conn:
    for disciplina, topico, subtopico in topicos_faltantes:
        # Verificar se já existe
        result = conn.execute(
            text("SELECT id FROM topics WHERE disciplina = :disc AND topico = :top"),
            {"disc": disciplina, "top": topico}
        )
        existing = result.fetchone()
        
        if existing:
            print(f"⚠️  Já existe: {disciplina} - {topico}")
        else:
            conn.execute(
                text("""
                    INSERT INTO topics (disciplina, topico, subtopico, reference)
                    VALUES (:disc, :top, :sub, :ref)
                """),
                {
                    "disc": disciplina,
                    "top": topico,
                    "sub": subtopico,
                    "ref": f"Edital IBGP - {disciplina}"
                }
            )
            conn.commit()
            print(f"✅ Criado: {disciplina} - {topico}")

print("\n🎉 Tópicos adicionados! Agora execute o comando para gerar as questões.")
