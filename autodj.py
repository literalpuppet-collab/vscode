#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import glob
import random
import socket
import subprocess

try:
    from mutagen.mp3 import MP3
except ImportError:
    print("[ERRO] Instale a biblioteca mutagen: pip3 install mutagen")
    sys.exit(1)

# Configurações do Servidor Shoutcast
HOST = "127.0.0.1"
PORT = 8000
PASSWORD = "thealphadio32"
MUSIC_DIR = "musicas"

SHOUTCAST_EXEC = "./sc_serv"
SHOUTCAST_CONF = "sc_serv.conf"

def start_shoutcast():
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

def get_mp3_list():
    files = glob.glob(os.path.join(MUSIC_DIR, "**", "*.mp3"), recursive=True)
    files += glob.glob(os.path.join(MUSIC_DIR, "**", "*.MP3"), recursive=True)
    files = list(set(files))
    if not files:
        print("[ERRO] Nenhum arquivo MP3 encontrado na pasta 'musicas'.")
        sys.exit(1)
    return files

def run_autodj():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.connect((HOST, PORT))

            # Autenticação ICY
            sock.sendall(f"{PASSWORD}\r\n".encode("utf-8"))
            
            response = sock.recv(1024).decode("utf-8", errors="ignore")
            if "OK" not in response and "ICY 200 OK" not in response:
                print(f"[ERRO] Autenticação falhou: {response.strip()}")
                sock.close()
                time.sleep(3)
                continue

            icy_headers = (
                "icy-name:AutoDJ Python\r\n"
                "icy-genre:Variado\r\n"
                "icy-pub:0\r\n"
                "icy-br:128\r\n"
                "content-type:audio/mpeg\r\n"
                "\r\n"
            )
            sock.sendall(icy_headers.encode("utf-8"))
            print("AutoDJ conectado ao Shoutcast com sucesso!")

            files = get_mp3_list()
            random.shuffle(files)

            chunk_size = 4096

            for f in files:
                print(f"Tocando: {os.path.basename(f)}")

                # Detecta o bitrate exato do arquivo atual
                try:
                    audio_info = MP3(f)
                    bitrate = audio_info.info.bitrate
                    bytes_per_sec = bitrate / 8
                except Exception:
                    bytes_per_sec = 16000  # Fallback para 128 kbps

                with open(f, "rb") as mp3:
                    start_stream_time = time.time()
                    total_bytes_sent = 0

                    while True:
                        data = mp3.read(chunk_size)
                        if not data:
                            break
                        
                        sock.sendall(data)
                        total_bytes_sent += len(data)

                        # Mantém a sincronização exata sem acumular atrasos
                        expected_time = total_bytes_sent / bytes_per_sec
                        actual_time = time.time() - start_stream_time

                        time_to_sleep = expected_time - actual_time
                        if time_to_sleep > 0:
                            time.sleep(time_to_sleep)

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
        print("\nEncerrando...")
    finally:
        shoutcast_process.terminate()
        shoutcast_process.wait()

if __name__ == "__main__":
    main()