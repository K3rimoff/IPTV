import re
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_new_hash():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ekran olmadan işlə
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://canlitv.com/kanal-d-canli-yayin"
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        
        # Player-i tapmaq və klikləmək (lazımdırsa)
        try:
            play_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jw-display-icon-container")))
            play_button.click()
            time.sleep(7) # Hash-in generasiya olunması üçün vaxt
        except:
            pass

        page_source = driver.page_source
        match = re.search(r'hash=([a-f0-9]+)', page_source)
        
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
    finally:
        driver.quit()
    return None

def update_m3u_file(new_hash):
    filename = "Tur.m3u"
    if not os.path.exists(filename):
        print(f"{filename} tapılmadı!")
        return

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    # M3U faylındakı bütün hash=... dəyərlərini yenisi ilə əvəz edirik
    # Regex: 'hash=' sözündən sonra gələn hərf və rəqəmləri hədəf alır
    new_content = re.sub(r'(hash=)[a-f0-9]+', r'\1' + new_hash, content)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(new_content)
    
    print(f"Fayl yeniləndi. Yeni hash: {new_hash}")

if __name__ == "__main__":
    current_hash = get_new_hash()
    if current_hash:
        update_m3u_file(current_hash)
    else:
        print("Hash əldə etmək mümkün olmadı.")
