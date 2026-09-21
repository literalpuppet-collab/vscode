FROM python:3.10-slim

# Instala o Liquidsoap, curl e bibliotecas necessárias para o Shoutcast
RUN apt-get update && apt-get install -y \
    liquidsoap \
    curl \
    libc6 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Cria o usuário não-root 'shoutcast'
RUN useradd -m shoutcast

WORKDIR /app

# Copia e instala as dependências do Python a partir do requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto para o container e ajusta as permissões
COPY . .
RUN chmod +x sc_serv start.sh && chown -R shoutcast:shoutcast /app

# Define o usuário que rodará o container
USER shoutcast

# Expõe a porta do servidor Shoutcast
EXPOSE 8000

CMD ["./start.sh"]
