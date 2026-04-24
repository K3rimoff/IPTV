import re
import requests

INPUT_FILE = "IPTV.m3u"
# Tokeni dinamik götürmək üçün rəsmi canlı yayım səhifəsini istifadə etmək daha yaxşıdır
SOURCE_PAGE = "https://aztv.az/az/live"

def get_fresh_token():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(SOURCE_PAGE, headers=headers, timeout=15)
        # Səhifə daxilindən tokeni tuturuq
        match = re.search(r'token=([a-zA-Z0-9._=-]+)', response.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Xəta: {e}")
    return None

def update_m3u(new_token):
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # BU HİSSƏ KİRİTİKDİR: 'token=' ilə başlayan və sətir sonuna və ya boşluğa qədər olan hər şeyi dəyişir
        updated_content = re.sub(r'token=[a-zA-Z0-9._=-]*', f'token={new_token}', content)

        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Uğurla yeniləndi: {new_token[:15]}...")
    except FileNotFoundError:
        print(f"Xəta: {INPUT_FILE} tapılmadı!")

if __name__ == "__main__":
    token = get_fresh_token()
    if token:
        update_m3u(token)
    else:
        print("Token tapılmadı!")
