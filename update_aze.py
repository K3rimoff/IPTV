import re
import requests

INPUT_FILE = "Aze.m3u"
# Tokeni götürəcəyimiz əsas səhifə
SOURCE_PAGE = "https://yoda.az/"

def get_fresh_token():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://yoda.az/'
    }
    try:
        response = requests.get(SOURCE_PAGE, headers=headers, timeout=15)
        response.raise_for_status()
        
        # data-token atributunun içindəki hər hansı simvol ardıcıllığını tam götürürük
        match = re.search(r'data-token=["\']([^"\']+)["\']', response.text)
        
        if match:
            return match.group(1)
        else:
            print("Token div daxilində tapılmadı.")
            # Ehtiyat variant
            alt_match = re.search(r'token=([^&\s"<>]+)', response.text)
            return alt_match.group(1) if alt_match else None
            
    except Exception as e:
        print(f"Bağlantı xətası: {e}")
    return None

def update_m3u(new_token):
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Fayldakı bütün köhnə tokenləri yenisi ilə əvəz edirik
        updated_content = re.sub(r'token=[^&\s"<>]*', f'token={new_token}', content)

        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Uğurlu! Yeni token tətbiq edildi: {new_token[:15]}...")
    except FileNotFoundError:
        print(f"Xəta: {INPUT_FILE} faylı tapılmadı!")

if __name__ == "__main__":
    token = get_fresh_token()
    if token:
        update_m3u(token)
    else:
        print("Token tapılmadı, yenilənmə baş tutmadı.")
