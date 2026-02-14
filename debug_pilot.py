import asyncio
import json
import os
import glob
from playwright.async_api import async_playwright

async def debug():
    cookie_path = sorted(glob.glob("cookies/*.json"))[0]
    video_path = sorted(glob.glob("output_videos/*.mp4"))[0]
    
    with open(cookie_path, 'r') as f:
        cookies = json.load(f)

    async with async_playwright() as p:
        # Proxy'siz deniyoruz ki sorun proxy kaynaklı mı anlayalım
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        # Cookie ekleme testi
        try:
            # Eğer liste değilse listeye alalım
            if isinstance(cookies, dict) and "cookies" in cookies: cookies = cookies["cookies"]
            await context.add_cookies(cookies)
        except Exception as e:
            print(f"❌ Cookie format hatası: {e}")
            return

        page = await browser.new_page()
        print(f"🌐 TikTok Studio açılıyor: {cookie_path}")
        await page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload")
        await page.wait_for_timeout(10000) # Sayfanın oturması için bekle
        
        # Ekran görüntüsü al
        await page.screenshot(path="debug_snap.png")
        print(f"📸 Ekran görüntüsü alındı: debug_snap.png")
        print(f"📍 Mevcut URL: {page.url}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug())
