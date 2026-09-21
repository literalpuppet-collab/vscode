#!/bin/bash

# A dey start da Shoutcast server na background
./sc_serv sc_serv.conf &

# A dey wet 2 sekɔn mek da port kin opin fine
sleep 2

# A dey start da AutoDJ we mek wikal Python script
python main.py