import asyncio
import json
import os
import glob
import shutil
from playwright.async_api import async_playwright

COOKIE_DIR = "cookies"
LIVE_DIR = "live_cookies"
BATCH_SIZE = 5 # Aynı anda 5 tarayıcı (RAM dostu)
os.makedirs(LIVE_DIR, exist_ok=True)

async def check_account(browser_context, cookie_path):
    try:
        with open(cookie_path, 'r') as f:
            cookies = json.load(f)
            if isinstance(cookies, dict) and "cookies" in cookies: cookies = cookies["cookies"]
            if not isinstance(cookies, list): cookies = [cookies]
            for c in cookies:
                if 'domain' not in c: c['domain'] = '.tiktok.com'
            await browser_context.add_cookies(cookies)

        page = await browser_context.new_page()
        # Manuel Stealth
        await browser_context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        await page.goto("https://www.tiktok.com/foryou", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(4)
        
        if "login" not in page.url and len(await page.content()) > 500:
            print(f"✅ CANLI: {os.path.basename(cookie_path)}")
            shutil.copy(cookie_path, os.path.join(LIVE_DIR, os.path.basename(cookie_path)))
        else:
            print(f"❌ ÖLÜ: {os.path.basename(cookie_path)}")
        await page.close()
    except:
        print(f"⚠️ HATA: {os.path.basename(cookie_path)}")

async def main():
    cookie_files = [f for f in glob.glob(f"{COOKIE_DIR}/*.json") if not os.path.exists(os.path.join(LIVE_DIR, os.path.basename(f)))]
    print(f"🔎 Toplam {len(cookie_files)} pilot kontrol bekliyor...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        # Her 5 hesapta bir context'i yenileyerek RAM'i taze tutuyoruz
        for i in range(0, len(cookie_files), BATCH_SIZE):
            batch = cookie_files[i:i+BATCH_SIZE]
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            tasks = [check_account(context, f) for f in batch]
            await asyncio.gather(*tasks)
            await context.close()
            print(f"--- BATCH {i//BATCH_SIZE + 1} TAMAMLANDI ---")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
