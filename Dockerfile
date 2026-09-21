FROM python:3.10-slim

# Instala o Icecast2 e o FFmpeg no sistema
RUN apt-get update && apt-get install -y \
    icecast2 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos do projeto para o container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Permissão para o script de inicialização
RUN chmod +x start.sh

# Expõe a porta do servidor de rádio
EXPOSE 8000

CMD ["./start.sh"]