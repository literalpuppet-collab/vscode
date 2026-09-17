#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import glob
import random
import socket
import subprocess

# Validação de bibliotecas externas
try:
    from mutagen.mp3 import MP3
except ImportError:
    print("[ERRO] Instale a biblioteca mutagen: pip3 install mutagen")
    sys.exit(1)

# =====================================================================
# CONFIGURAÇÕES DO AUTODJ E DO SERVIDOR
# =====================================================================
HOST = "127.0.0.1"
PORT = 8000
PASSWORD = "thealphadio32"
MUSIC_DIR = "Musicas"  # Ajustado conforme a pasta no seu GitHub (case-sensitive no Linux)

# Executável e arquivo de configuração do Shoutcast
SHOUTCAST_EXEC = "./sc_serv"
SHOUTCAST_CONF = "sc_serv.conf"
# =====================================================================


def start_shoutcast():
    """Inicia o servidor Shoutcast em segundo plano."""
    print("Iniciando o servidor Shoutcast...")
    try:
        proc = subprocess.Popen(
            [SHOUTCAST_EXEC, SHOUTCAST_CONF],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
        return proc
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao iniciar o Shoutcast: {e}")
        sys.exit(1)


def get_music_list():
    """Busca qualquer tipo de arquivo de música suportado na pasta."""
    extensions = ["*.mp3", "*.MP3", "*.wav", "*.WAV", "*.ogg", "*.OGG", "*.aac", "*.AAC", "*.flac", "*.FLAC", "*.m4a", "*.M4A", "*.mp4", "*.MP4"]
    files = []

    for ext in extensions:
        files.extend(glob.glob(os.path.join(MUSIC_DIR, "**", ext), recursive=True))

    files = list(set(files))
    if not files:
        print(f"[ERRO] Nenhum arquivo de música encontrado na pasta '{MUSIC_DIR}'.")
        sys.exit(1)
    return files


def transmitir_arquivo_audio(sock, caminho_arquivo):
    """Lê e envia um arquivo de áudio pelo socket mantendo o tempo correto."""
    chunk_size = 4096

    try:
        audio_info = MP3(caminho_arquivo)
        bitrate = audio_info.info.bitrate
        bytes_per_sec = bitrate / 8
    except Exception:
        bytes_per_sec = 16000  # Fallback padrão (128 kbps)

    with open(caminho_arquivo, "rb") as audio:
        start_stream_time = time.time()
        total_bytes_sent = 0

        while True:
            data = audio.read(chunk_size)
            if not data:
                break

            sock.sendall(data)
            total_bytes_sent += len(data)

            expected_time = total_bytes_sent / bytes_per_sec
            actual_time = time.time() - start_stream_time

            time_to_sleep = expected_time - actual_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)


def run_autodj():
    """Executa o loop contínuo da transmissão sem repetir músicas no mesmo ciclo."""
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.connect((HOST, PORT))

            sock.sendall(f"{PASSWORD}\r\n".encode("utf-8"))
            
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "OK" not in response and "ICY 200 OK" not in response:
                print(f"[ERRO] Autenticação falhou: {response.strip()}")
                sock.close()
                time.sleep(3)
                continue

            # Nome da rádio alterado para "The AlphaCraft Rádio"
            icy_headers = (
                "icy-name:The AlphaCraft Rádio\r\n"
                "icy-genre:Variado\r\n"
                "icy-pub:0\r\n"
                "icy-br:128\r\n"
                "content-type:audio/mpeg\r\n"
                "\r\n"
            )
            sock.sendall(icy_headers.encode("utf-8"))
            print("AutoDJ conectado ao Shoutcast com sucesso! (The AlphaCraft Rádio)")

            while True:
                files = get_music_list()

                # Embaralha todas as músicas aleatoriamente para o novo ciclo
                random.shuffle(files)
                print(f"\n--- [NOVO CICLO DA PLAYLIST] {len(files)} músicas encontradas na fila ---")

                # Toca cada música da lista uma única vez
                for index, f in enumerate(files, 1):
                    print(f"[{index}/{len(files)}] Tocando: {os.path.basename(f)}")
                    transmitir_arquivo_audio(sock, f)

                print("\n[PLAYLIST FINALIZADA] Todas as músicas do ciclo foram tocadas.")
                print("Reiniciando a lista com uma nova ordem aleatória...\n")

        except (socket.error, ConnectionRefusedError):
            print("Servidor indisponível. Reconectando em 3s...")
            time.sleep(3)
        except Exception as e:
            print(f"Erro no AutoDJ: {e}")
            time.sleep(3)


def main():
    shoutcast_process = start_shoutcast()
    try:
        run_autodj()
    except KeyboardInterrupt:
        print("\nEncerrando AutoDJ e finalizando o Shoutcast...")
    finally:
        shoutcast_process.terminate()
        shoutcast_process.wait()
        print("Servidor finalizado com sucesso.")


if __name__ == "__main__":
    main()