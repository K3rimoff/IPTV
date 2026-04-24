import re

INPUT_FILE = "IPTV.m3u"
OUTPUT_FILE = "IPTV.m3u"

# Səndə olan istənilən working linkdən token götür
SOURCE_LINK = "https://str.yodacdn.net/azertv/index.m3u8?token=..."

def extract_token(url):
    match = re.search(r'token=(.*)', url)
    return match.group(1) if match else None

def update_m3u(token):
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r'token=__TOKEN__', f'token={token}', content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    token = extract_token(SOURCE_LINK)
    if token:
        update_m3u(token)
        print("Updated successfully")
    else:
        print("Token not found")

if __name__ == "__main__":
    main()
