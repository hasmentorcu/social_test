import asyncio
import os
import aiohttp
from playwright.async_api import async_playwright

# --- AYARLAR ---
PROXY_RESET_URL = "https://v.veloproxy.net/r/atakigaurvxfqxlvrsov"
PROXY_SERVER = "http://31.59.131.46:11708"
PROXY_AUTH = {"username": "u2081", "password": "tl9Z7pbLFZil"}
ACCOUNTS_FILE = "basarili_pilotlar.txt"

if not os.path.exists("cookies"): os.makedirs("cookies")
if not os.path.exists("hasat_hatalari"): os.makedirs("hasat_hatalari")

async def rotate_ip():
    print("\n🔄 IP Yenileniyor (VeloProxy)...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(PROXY_RESET_URL, timeout=15) as response:
                print(f"📡 Reset Sinyali Gönderildi: Durum {response.status}")
            await asyncio.sleep(35) # Hattın oturması için zaman
        except Exception as e:
            print(f"⚠️ Proxy Reset Hatası: {e}")

async def harvest():
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"❌ {ACCOUNTS_FILE} bulunamadı!")
        return

    with open(ACCOUNTS_FILE, "r") as f:
        accounts = [line.strip() for line in f if ":" in line]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        
        for account in accounts:
            email, password = account.split(":")
            cookie_path = f"cookies/{email}.json"
            if os.path.exists(cookie_path): continue

            print(f"🚜 Hasat Sırası: {email}")
            await rotate_ip()

            context = await browser.new_context(
                proxy={"server": PROXY_SERVER, "username": PROXY_AUTH["username"], "password": PROXY_AUTH["password"]},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            try:
                print(f"📡 {email} için giriş sayfasına gidiliyor...")
                await page.goto("https://www.tiktok.com/login/phone-or-email/email", timeout=90000, wait_until="load")
                
                # 🍪 Mavi Banner'ı Temizle
                try:
                    allow_all = page.locator('button:has-text("Allow all")')
                    if await allow_all.is_visible(timeout=10000):
                        await allow_all.click()
                        print("🍪 Banner kapatıldı.")
                except: pass

                # 🎯 Giriş Bilgilerini Yaz
                user_input = page.locator('input[name="username"], input[name="email"], input[placeholder*="Email"]')
                await user_input.wait_for(state="visible", timeout=30000)
                await user_input.fill(email)
                await page.locator('input[type="password"]').fill(password)
                await page.click('button[type="submit"]')
                
                print("⏳ Oturum açılması bekleniyor...")
                await asyncio.sleep(20) 

                await context.storage_state(path=cookie_path)
                print(f"✅ {email} mühürlendi.")

            except Exception as e:
                print(f"❌ Hata: {str(e)[:50]}")
                await page.screenshot(path=f"hasat_hatalari/{email}.png")
            finally:
                await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(harvest())
