import requests
import re

# 1. Saytdan yeni linki/tokeni götürmək
# Qeyd: Burada linkin yerləşdiyi səhifənin URL-ni daxil edin
SOURCE_URL = "YENI_LINKIN_OLDUGU_SAYT_URL" 

def get_new_token_link():
    response = requests.get(SOURCE_URL)
    if response.status_code == 200:
        # Burada Regex vasitəsilə linki axtarırıq. 
        # Sizin nümunəyə uyğun pattern (nümunədir, sayta görə dəyişə bilər):
        pattern = r'https://str\.yodacdn\.net/xazartv/tracks-v1a1/mono\.ts\.m3u8\?token=[\w\.-]+'
        match = re.search(pattern, response.text)
        if match:
            return match.group(0)
    return None

# 2. m3u faylını yeniləmək
new_link = get_new_token_link()

if new_link:
    with open("playlist.m3u", "r") as file:
        lines = file.readlines()

    with open("playlist.m3u", "w") as file:
        for line in lines:
            # Köhnə linki yenisi ilə əvəz et (Kanal adından sonrakı sətri tapır)
            if "xazartv" in line:
                file.write(new_link + "\n")
            else:
                file.write(line)
    print("Link uğurla yeniləndi.")
else:
    print("Yeni link tapılmadı.")
