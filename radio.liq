# Configurações de log
set("log.stdout", true)

# Carrega as variáveis de ambiente com fallback padrão
music_dir = environment.get(default="musicas", "MUSIC_DIR")
shout_host = environment.get(default="127.0.0.1", "SHOUTCAST_HOST")
shout_port = string.to_int(environment.get(default="8000", "SHOUTCAST_PORT"))
shout_pass = environment.get(default="thealphadio32", "SHOUTCAST_PASSWORD")

# 1. Carrega a playlist a partir da pasta e sorteia as faixas
playlist_musicas = playlist(music_dir, mode="randomize")

# 2. Garante transmissão contínua mesmo se a playlist falhar
radio = mksafe(playlist_musicas)

# 3. Transmite via Shoutcast/Icecast em MP3 128kbps
output.shoutcast(%mp3(bitrate=128),
  host = shout_host,
  port = shout_port,
  password = shout_pass,
  name = "The AlphaCraft Radio",
  url = "http://127.0.0.1:8000",
  genre = "Varied",
  radio
)