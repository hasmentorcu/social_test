import asyncio
import json
import os
import random
import glob
import requests
from playwright.async_api import async_playwright

# --- AYARLAR ---
LIVE_COOKIE_DIR = "live_cookies"
VIDEO_DIR = "output_videos"
PROXY_URL = "http://u2081:tl9Z7pbLFZil@31.59.131.46:11708"
ROTATE_URL = "https://v.veloproxy.net/r/atakigaurvxfqxlvrsov"

def refresh_ip():
    print("🔄 IP adresi yenileniyor...")
    try:
        r = requests.get(ROTATE_URL, timeout=15)
        print(f"📡 IP Yenileme Yanıtı: {r.text.strip()}")
        return True
    except:
        return False

async def upload_to_tiktok(p, cookie_path, video_path):
    pilot_id = os.path.basename(cookie_path)
    print(f"\n✈️  Pilot Göreve Başlıyor: {pilot_id}")
    
    refresh_ip()
    # Modemin kendine gelmesi için süreyi artırdık
    await asyncio.sleep(15) 

    browser = await p.chromium.launch(headless=True, args=[
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
    ])
    
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        proxy={"server": PROXY_URL},
        viewport={'width': 1280, 'height': 720}
    )

    try:
        page = await context.new_page()
        
        # RAM DOSTU: Resim, Font ve Medyayı engelle
        await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,otf,ttf}", lambda route: route.abort())

        with open(cookie_path, 'r') as f:
            cookies = json.load(f)
            if isinstance(cookies, dict) and "cookies" in cookies: cookies = cookies["cookies"]
            for c in cookies: 
                c['domain'] = '.tiktok.com'
                c['secure'] = True
            await context.add_cookies(cookies)

        # wait_until="commit" yaparak sayfanın tamamen render edilmesini beklemiyoruz, bu çok hızlandırır
        print("🏠 Ana sayfaya sızılıyor (Medya engellendi)...")
        await page.goto("https://www.tiktok.com/", wait_until="commit", timeout=60000)
        await asyncio.sleep(8)

        print("🚀 Yükleme sayfasına geçiliyor...")
        await page.goto("https://www.tiktok.com/upload?lang=tr-TR", wait_until="domcontentloaded", timeout=60000)
        
        if "login" in page.url:
            print(f"❌  OTURUM ÖLMÜŞ: {pilot_id}")
            return False

        print(f"📁  Video basılıyor: {os.path.basename(video_path)}")
        file_input = page.locator('input[type="file"]')
        await file_input.set_input_files(video_path)
        
        print("⏳  İşleme bekleniyor...")
        publish_button = page.get_by_test_id("post-publish-button")
        # Video yüklenirken resimler kapalı olsa da buton aktifleşecektir
        await publish_button.wait_for(state="visible", timeout=120000)
        
        await asyncio.sleep(10)
        await publish_button.click()
        print(f"✅  HEDEF VURULDU: {pilot_id} videoyu bastı!")
        
        if os.path.exists(video_path):
            os.remove(video_path)
        return True

    except Exception as e:
        print(f"⚠️  Hata: {str(e)[:150]}")
        return False
    finally:
        await browser.close()

async def main():
    pilots = glob.glob(f"{LIVE_COOKIE_DIR}/*.json")
    async with async_playwright() as p:
        for pilot in pilots:
            videos = glob.glob(f"{VIDEO_DIR}/*.mp4")
            if not videos:
                print("🛑 Mermi bitti!")
                break
            success = await upload_to_tiktok(p, pilot, videos[0])
            if success:
                # Başarılı yükleme sonrası 8-12 dk mola (IP sağlığı için)
                wait = random.randint(480, 720)
                print(f"💤  Başarı Molası: {wait} saniye...")
                await asyncio.sleep(wait)
            else:
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
