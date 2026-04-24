import requests
import re
import os

# Tokeni çəkəcəyimiz mənbə
SOURCE_URL = "https://aztv.az/az/live"
M3U_FILENAME = "playlist.m3u"

def get_latest_token():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # HTML daxilində tokeni axtarırıq
        # Yoda CDN adətən tokeni bu formatda verir
        match = re.search(r'token=([a-zA-Z0-9._=-]+)', response.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Token alınarkən xəta: {e}")
    return None

def update_m3u_file(new_token):
    if not os.path.exists(M3U_FILENAME):
        print(f"Fayl tapılmadı: {M3U_FILENAME}")
        return

    with open(M3U_FILENAME, 'r', encoding='utf-8') as f:
        content = f.read()

    # Bütün 'token=...' hissələrini tapıb yeni tokenlə əvəz edirik
    # Regex: 'token=' sözündən başlayıb növbəti boşluğa və ya sətir sonuna qədər olan hissə
    updated_content = re.sub(r'token=[a-zA-Z0-9._=-]+', f'token={new_token}', content)

    with open(M3U_FILENAME, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("M3U siyahısı uğurla yeniləndi.")

if __name__ == "__main__":
    token = get_latest_token()
    if token:
        print(f"Yeni token tapıldı: {token[:15]}...")
        update_m3u_file(token)
    else:
        print("Təəssüf, yeni token tapılmadı.")
