import os
import random
import time
import shutil
import json
import requests
from playwright.sync_api import sync_playwright

# --- KONFİGÜRASYON ---
PROXY_SERVER = "http://31.59.131.46:11708" 
PROXY_USER = "u2081"
PROXY_PASS = "tl9Z7pbLFZil"
IP_REFRESH_URL = "https://v.veloproxy.net/r/atakigaurvxfqxlvrsov"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_DIR = os.path.join(BASE_DIR, "cookies") # Harvester'ın kayıt yeri
VIDEO_DIR = os.path.join(BASE_DIR, "factory/output_videos")
ARCHIVE_DIR = os.path.join(BASE_DIR, "factory/archive")

def refresh_ip():
    print(f"\n🔄 VELOPROXY: IP tazeleniyor...")
    try:
        requests.get(IP_REFRESH_URL, timeout=15)
        time.sleep(15) 
    except: pass

def get_caption(filename):
    try:
        clean = filename.split("_", 2)[2].replace(".mp4", "").replace("_", " ").upper()
        return f"{clean} #fyp #viral #kesfet"
    except: return "New Pilot Video #fyp"

def mass_upload():
    # 1. Cookie dosyalarını kontrol et
    cookie_files = [f for f in os.listdir(COOKIES_DIR) if f.endswith(".json")]
    if not cookie_files: return print(f"❌ '{COOKIES_DIR}' içinde cookie bulunamadı!")

    videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
    if not videos: return print("❌ Video stoğu bitti.")

    print(f"⚔️ COOKIE OPERASYONU: {len(cookie_files)} Hesap, {len(videos)} Video")

    with sync_playwright() as p:
        for i, c_file in enumerate(cookie_files):
            if not videos: break
            
            refresh_ip()
            video_file = videos[0]
            account_name = c_file.replace(".json", "")
            print(f"👤 [{i+1}/{len(cookie_files)}] HESAP: {account_name}")

            browser = p.chromium.launch(
                headless=True,
                proxy={"server": PROXY_SERVER, "username": PROXY_USER, "password": PROXY_PASS},
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            
            # Context'i doğrudan Cookie ile oluştur
            cookie_path = os.path.join(COOKIES_DIR, c_file)
            context = browser.new_context(
                storage_state=cookie_path, # HARVESTER'DAN GELEN DOSYA
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = context.new_page()

            try:
                # GİRİŞİ ATLA, DOĞRUDAN UPLOAD'A GİT
                print("📤 Doğrudan Upload merkezine gidiliyor...")
                page.goto("https://www.tiktok.com/tiktokstudio/upload?lang=en", wait_until="load", timeout=90000)
                time.sleep(10)

                # Eğer hala login istiyorsa cookie patlamıştır
                if "login" in page.url:
                    print(f"❌ {account_name} için Cookie geçersiz!")
                    continue

                # DOSYA YÜKLE
                input_selector = 'input[type="file"]'
                # Iframe kontrolü
                iframe = page.frame_locator('iframe[src*="creator"]').first
                target = iframe if iframe.locator(input_selector).count() > 0 else page
                
                if target.locator(input_selector).count() > 0:
                    target.locator(input_selector).set_input_files(os.path.join(VIDEO_DIR, video_file))
                    print("✅ Video enjekte edildi.")
                    time.sleep(20) # Yükleme süresi
                    
                    # Başlık ve Paylaş
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    page.keyboard.type(get_caption(video_file))
                    
                    time.sleep(5)
                    post_btn = page.locator('button:has-text("Post"), button:has-text("Yayınla")').first
                    if post_btn.is_enabled():
                        post_btn.click()
                        print(f"🚀 PAYLAŞILDI: {account_name}")
                        shutil.move(os.path.join(VIDEO_DIR, video_file), os.path.join(ARCHIVE_DIR, video_file))
                        videos.pop(0)
                    else:
                        print("❌ Paylaş butonu aktif değil.")
                else:
                    print("❌ Yükleme alanı bulunamadı (Studio yüklenemedi).")

            except Exception as e:
                print(f"❌ HATA: {e}")
                page.screenshot(path=f"factory/cookie_fail_{account_name}.png")
            
            finally:
                browser.close()
                time.sleep(5)

if __name__ == "__main__":
    mass_upload()
