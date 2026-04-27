import re
import requests

INPUT_FILE = "Tur.m3u"
# Hash-i götürəcəyimiz mənbə səhifə (Show TV kanalı üzərindən)
SOURCE_PAGE = "https://canlitv.com/show-tv-izle-1"

def get_fresh_hash():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://canlitv.com/'
    }
    try:
        response = requests.get(SOURCE_PAGE, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Regex: jwplayer daxilindəki hash= kodunu tapır
        # file: "....m3u8?hash=6b62e7..."
        match = re.search(r'hash=([a-zA-Z0-9]+)', response.text)
        
        if match:
            new_hash = match.group(1)
            print(f"Yeni Hash tapıldı: {new_hash}")
            return new_hash
        else:
            print("Hash kodu saytın daxilində tapılmadı.")
            return None
            
    except Exception as e:
        print(f"Səhifəyə bağlanarkən xəta yarandı: {e}")
    return None

def update_m3u(new_hash):
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Fayldakı bütün köhnə hash-ləri yenisi ilə əvəz edirik
        # Bu regex 'hash=' ilə başlayıb növbəti simvola qədər olan hissəni tapır
        updated_content = re.sub(r'hash=[a-zA-Z0-9]+', f'hash={new_hash}', content)

        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Uğurlu! Tur.m3u faylındakı bütün linklər yeniləndi.")
        
    except FileNotFoundError:
        print(f"Xəta: {INPUT_FILE} faylı tapılmadı!")

if __name__ == "__main__":
    current_hash = get_fresh_hash()
    if current_hash:
        update_m3u(current_hash)
    else:
        print("Yenilənmə dayandırıldı.")
