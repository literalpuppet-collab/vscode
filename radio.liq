# Configurações de log
settings.log.stdout.set(true)

# Variáveis de ambiente
music_dir = environment.get(default="musicas", "MUSIC_DIR")
shout_host = environment.get(default="127.0.0.1", "SHOUTCAST_HOST")
shout_port = string.to_int(environment.get(default="8000", "SHOUTCAST_PORT"))
shout_pass = environment.get(default="thealphadio32", "SHOUTCAST_PASSWORD")

# 1. Carrega a playlist
playlist_musicas = playlist(music_dir, mode="randomize")

# 2. Formata e insere o metadado que o Shoutcast/Bot lê
def formatar_metadados(m) =
  title = m["title"]
  artist = m["artist"]
  # Pega só o nome do arquivo (sem caminho e sem extensão)
  filename = path.remove_extension(path.basename(m["filename"]))
  
  # Define o título que aparecerá no Discord / Players
  display_title = if title != "" then "#{artist} - #{title}" else filename end
  
  # Retorna o dicionário de metadados com o campo 'title' atualizado
  [("title", display_title)]
end

# Aplica a reescrita de metadados na fonte de áudio
radio_com_meta = metadata.map(formatar_metadados, playlist_musicas)

# 3. Garante transmissão contínua
radio = mksafe(radio_com_meta)

# 4. Transmite para o Shoutcast com os metadados mapeados
output.shoutcast(%mp3(bitrate=128),
  host = shout_host,
  port = shout_port,
  password = shout_pass,
  name = "The AlphaCraft Radio",
  url = "http://127.0.0.1:8000",
  genre = "Varied",
  radio
)
