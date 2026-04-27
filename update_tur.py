import re
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

INPUT_FILE = Path("Tur.m3u")
URL = "https://canlitv.com/show-tv-izle-1"


async def get_hash():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL, timeout=60000)

        # səhifənin tam yüklənməsini gözlə
        await page.wait_for_timeout(5000)

        content = await page.content()

        await browser.close()

        match = re.search(
            r'file:\s*"https?://[^"]+hash=([a-zA-Z0-9]+)',
            content
        )

        if match:
            return match.group(1)

        return None


def update_m3u(new_hash):
    if not INPUT_FILE.exists():
        print("M3U tapılmadı")
        return False

    content = INPUT_FILE.read_text(encoding="utf-8")

    updated, count = re.subn(
        r'hash=[a-zA-Z0-9]+',
        f'hash={new_hash}',
        content
    )

    INPUT_FILE.write_text(updated, encoding="utf-8")

    print(f"{count} link yeniləndi")
    return count > 0


async def main():
    new_hash = await get_hash()

    if not new_hash:
        print("Hash tapılmadı")
        return

    print("Yeni hash:", new_hash)

    updated = update_m3u(new_hash)

    if updated:
        print("Fayl yeniləndi")
    else:
        print("Dəyişiklik olmadı")


if __name__ == "__main__":
    asyncio.run(main())
