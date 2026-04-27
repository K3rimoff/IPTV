import re
import requests

INPUT_FILE = "Tur.m3u"
# Hash-i götürəcəyimiz mənbə səhifə
SOURCE_PAGE = "https://canlitv.com/show-tv-izle-1"

def get_fresh_hash():
    # Saytın bot olduğumuzu anlamaması üçün daha geniş başlıqlar əlavə edirik
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://canlitv.com/',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    try:
        response = requests.get(SOURCE_PAGE, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Səhifənin gəlib-gəlmədiyini yoxlayaq
        html_content = response.text
        
        # Regex-i daha spesifik edirik: 
        # 'file:' sözündən sonra gələn və içində 'hash=' olan m3u8 linkini axtarırıq
        match = re.search(r'file:\s*"(https?://[^"]+hash=([a-zA-Z0-9]+))"', html_content)
        
        if match:
            # match.group(2) birbaşa hash-in özünü verir
            new_hash = match.group(2)
            print(f"✅ Uğurla tapıldı! Yeni Hash: {new_hash}")
            return new_hash
        else:
            # Alternativ: Əgər yuxarıdakı tapmasa, daha bəsit bir axtarış yoxlayaq
            print("⚠️ Birinci regex tapmadı, alternativ yoxlanılır...")
            alt_match = re.search(r'hash=([a-zA-Z0-9]{32})', html_content)
            if alt_match:
                return alt_match.group(1)
            
            print("❌ Hash kodu HTML daxilində tapılmadı.")
            # Xəta anında HTML-in bir hissəsini çap edirik ki, problem nədir görək (Debug)
            print("Gələn HTML-in bir hissəsi:", html_content[:500])
            return None
            
    except Exception as e:
        print(f"🆘 Bağlantı xətası: {e}")
    return None

def update_m3u(new_hash):
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Fayldakı bütün hash=... hissələrini yenisi ilə əvəz edirik
        updated_content = re.sub(r'hash=[a-zA-Z0-9]+', f'hash={new_hash}', content)

        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"🚀 {INPUT_FILE} faylındakı bütün linklər yeniləndi.")
        
    except FileNotFoundError:
        print(f"Xəta: {INPUT_FILE} faylı tapılmadı!")

if __name__ == "__main__":
    current_hash = get_fresh_hash()
    if current_hash:
        update_m3u(current_hash)
    else:
        print("🛑 Yenilənmə baş tutmadı.")
