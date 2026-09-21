#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import time
import random
import subprocess

MUSIC_DIR = os.getenv("MUSIC_DIR", "Musicas")
ICECAST_PASS = os.getenv("ICECAST_PASSWORD", "thealphadio32")
ICECAST_HOST = os.getenv("ICECAST_HOST", "127.0.0.1")
ICECAST_PORT = os.getenv("ICECAST_PORT", "8000")

def get_music_list():
    extensions = ["*.mp3", "*.MP3", "*.wav", "*.WAV", "*.ogg", "*.OGG", "*.aac", "*.AAC", "*.flac", "*.FLAC", "*.m4a", "*.M4A"]
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(MUSIC_DIR, "**", ext), recursive=True))
    files = list(set(files))
    if not files:
        print(f"[ERRO] Nenhum arquivo de música encontrado na pasta '{MUSIC_DIR}'.")
        sys.exit(1)
    return files

def main():
    print("Iniciando AutoDJ com FFmpeg...")
    
    while True:
        files = get_music_list()
        random.shuffle(files)
        
        # Cria uma playlist temporária para o FFmpeg
        with open("playlist.txt", "w", encoding="utf-8") as f:
            for item in files:
                f.write(f"file '{os.path.abspath(item)}'\n")

        # Transmite a playlist completa reencodando em 128kbps no formato ICY/Icecast
        cmd = [
            "ffmpeg",
            "-re",
            "-f", "concat",
            "-safe", "0",
            "-i", "playlist.txt",
            "-acodec", "libmp3lame",
            "-ab", "128k",
            "-ar", "44100",
            "-content_type", "audio/mpeg",
            "-f", "mp3",
            f"icecast://source:{ICECAST_PASS}@{ICECAST_HOST}:{ICECAST_PORT}/stream"
        ]

        print("Iniciando transmissão via FFmpeg...")
        process = subprocess.run(cmd)
        
        if process.returncode != 0:
            print("Erro ou término da transmissão. Reiniciando em 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    main()
