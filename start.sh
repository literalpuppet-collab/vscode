#!/bin/bash

# Inicia o Icecast2 em segundo plano
icecast2 -b -c /etc/icecast2/icecast.xml

# Aguarda o serviço iniciar a porta
sleep 2

# Inicia o AutoDJ em Python
python autodj.py