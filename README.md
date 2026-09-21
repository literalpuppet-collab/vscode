#asas

sas
# The AlphaCraft Rádio - AutoDJ

Servidor de streaming de áudio automatizado utilizando Python, Icecast2 e FFmpeg.

## Estrutura do Projeto
- `Musicas/`: Diretório onde devem ser salvos os arquivos de áudio.
- `autodj.py`: Script principal responsável pelo gerenciamento da playlist.
- `Dockerfile`: Arquivo de configuração para deploy em plataformas cloud (Railway, Render, Fly.io).

## Como Executar
1. Coloque os arquivos de música na pasta `Musicas/`.
2. Faça o deploy em seu provedor cloud via Dockerfile.