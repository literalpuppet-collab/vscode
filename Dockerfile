FROM python:3.10-slim

# Instala o FFmpeg, curl e bibliotecas necessárias para rodar o binário do Shoutcast no Linux
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    libc6 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos do projeto para o container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Da permissao de execucao para o binario do Shoutcast e o script de inicializacao
RUN chmod +x sc_serv start.sh

# Expoe a porta do servidor Shoutcast
EXPOSE 8000

CMD ["./start.sh"]