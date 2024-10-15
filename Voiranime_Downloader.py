#episode 1 de komi cherche ses mots (download cette fois)

from function.__init__ import *

print(Cardinal.Analyse())

import subprocess

# URL du fichier .m3u8
m3u8_url = "https://box-1006-u.vmeas.cloud/hls/xqx2oumporokjiqbteqsjpi4upwkf6ljtplojo4tqweelqybn74ojdkxerwq/index-v1-a1.m3u8"

# Fichier de sortie
output_file = "output_video.mp4"

# En-têtes HTTP à utiliser
headers = (
    "Accept: */*\r\n"
    "Accept-Encoding: gzip, deflate, br, zstd\r\n"
    "Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7\r\n"
    "Connection: keep-alive\r\n"
    "Host: box-1006-u.vmeas.cloud\r\n"
    "Origin: https://vidmoly.to\r\n"
    "Referer: https://vidmoly.to/\r\n"
    "Sec-Fetch-Dest: empty\r\n"
    "Sec-Fetch-Mode: cors\r\n"
    "Sec-Fetch-Site: cross-site\r\n"
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0\r\n"
    'sec-ch-ua: "Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"\r\n'
    'sec-ch-ua-mobile: ?0\r\n'
    'sec-ch-ua-platform: "Windows"\r\n'
)

# Commande ffmpeg avec en-têtes
ffmpeg_command = [
    'ffmpeg', 
    '-headers', headers, 
    '-i', m3u8_url, 
    '-c', 'copy', 
    output_file
]

# Exécuter la commande avec subprocess
# try:
#     result = subprocess.run(ffmpeg_command, check=True, text=True, capture_output=True)
#     print(f"Commande exécutée avec succès : {result.stdout}")
# except subprocess.CalledProcessError as e:
#     print(f"Erreur lors de l'exécution : {e.stderr}")
