#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess

# Configurações de comandos
SHOUTCAST_CMD = os.getenv("SHOUTCAST_CMD", "./sc_serv sc_serv.conf")
LIQUIDSOAP_CMD = os.getenv("LIQUIDSOAP_CMD", "liquidsoap radio.liq")


def iniciar_shoutcast():
    """Inicia o servidor Shoutcast em segundo plano."""
    print(f"[SHOUTCAST] Iniciando servidor: '{SHOUTCAST_CMD}'...")
    try:
        proc = subprocess.Popen(
            SHOUTCAST_CMD,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[SHOUTCAST] Servidor rodando em segundo plano!")
        time.sleep(3)  # Aguarda o servidor abrir a porta
        return proc
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar o Shoutcast: {e}")
        sys.exit(1)


def main():
    # 1. Inicia o Shoutcast
    shoutcast_proc = iniciar_shoutcast()

    print(f"[AUTODJ] Executando Liquidsoap: '{LIQUIDSOAP_CMD}'...")
    try:
        # 2. Roda o Liquidsoap em primeiro plano
        subprocess.run(LIQUIDSOAP_CMD, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Parando AutoDJ e Shoutcast...")
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Liquidsoap encerrou com erro: {e}")
    finally:
        # 3. Mata o Shoutcast ao fechar o script
        if shoutcast_proc and shoutcast_proc.poll() is None:
            print("[SHOUTCAST] Encerrando servidor Shoutcast...")
            shoutcast_proc.terminate()


if __name__ == "__main__":
    main()