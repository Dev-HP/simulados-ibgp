FROM python:3.11-slim

# Criar usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python como root (necessário para instalação)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código e ajustar permissões
COPY . .
RUN chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
