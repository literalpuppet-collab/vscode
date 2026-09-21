FROM python:3.10-slim

# Instala o Liquidsoap, curl e bibliotecas necessárias para o Shoutcast
RUN apt-get update && apt-get install -y \
    liquidsoap \
    curl \
    libc6 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala as dependências do Python a partir do requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto para o container
COPY . .

# Dá permissão de execução para o binário do Shoutcast e o script de inicialização
RUN chmod +x sc_serv start.sh

# Expõe a porta do servidor Shoutcast
EXPOSE 8000

CMD ["./start.sh"]
