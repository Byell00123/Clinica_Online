# Usa uma imagem oficial leve do Python
FROM python:3.12-slim

# Define variáveis de ambiente cruciais
# Evita que o Python escreva arquivos .pyc no container
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que o output do console seja exibido em tempo real
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências corretas para o MySQL
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código do projeto para o container
COPY . /app/

# Torna o script executável (caso não tenha permissão)
RUN chmod +x /app/entrypoint.sh

# Define o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]