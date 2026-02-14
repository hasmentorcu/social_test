import asyncio
import secrets
import random
import requests
import os
from playwright.async_api import async_playwright

# --- VELOPROXY LOJİSTİK HATTI ---
PROXY_RESET_URL = "https://v.veloproxy.net/r/atakigaurvxfqxlvrsov"
PROXY_SERVER = "http://31.59.131.46:11708"
PROXY_AUTH = {"username": "u2081", "password": "tl9Z7pbLFZil"}
MAIL_DOMAIN = "@ikihavaci.com.tr"

# Çerez klasörünü kontrol et, yoksa oluştur
if not os.path.exists("cookies"):
    os.makedirs("cookies")

async def rotate_ip():
    print("\n🔄 IP Yenileniyor (VeloProxy Hattı)...")
    try:
        requests.get(PROXY_RESET_URL, timeout=15)
        # 17 yıllık tecrübene dayanarak: IP'nin tam oturması için 25 sn idealdir
        print("⏳ Yeni IP'nin oturması bekleniyor (25 sn)...")
        await asyncio.sleep(25)
    except Exception as e:
        print(f"⚠️ Proxy Reset Hatası: {e}")

async def run_factory():
    async with async_playwright() as p:
        # Sunucu dostu, RAM korumalı tarayıcı ayarları
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        
        print(f"🚀 Üretim hattı {PROXY_SERVER} üzerinden mermi basmaya hazır.")

        while True:
            await rotate_ip()
            email_addr = f"{secrets.token_hex(4)}{MAIL_DOMAIN}"
            password = f"Ka{random.randint(100,999)}!!"
            
            # Her pilot için taze bir context (Session mühürleme burada başlar)
            context = await browser.new_context(
                proxy={
                    "server": PROXY_SERVER, 
                    "username": PROXY_AUTH["username"], 
                    "password": PROXY_AUTH["password"]
                },
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                print(f"🎯 HEDEF: {email_addr} | 📡 Sızılıyor...")
                
                # 'commit' ile hızı artırıyoruz, timeout'u esnek tutuyoruz
                await page.goto(
                    "https://www.tiktok.com/signup/phone-or-email/email", 
                    wait_until="commit", 
                    timeout=60000
                )
                
                # Formun yüklenmesini bekle
                email_input = page.locator('input[name="email"]')
                await email_input.wait_for(state="visible", timeout=20000)
                
                # --- Veri Girişi Operasyonu ---
                await email_input.fill(email_addr)
                await asyncio.sleep(1)
                await page.locator('input[type="password"]').fill(password)
                
                # 💡 NOT: Eğer doğum tarihi sayfası çıkarsa buraya manuel müdahale gerekebilir.
                
                print(f"✅ {email_addr} verileri girildi.")
                
                # KRİTİK ADIM: Gündüz vardiyası için session (cookie) bilgilerini kaydet
                cookie_path = f"cookies/{email_addr}.json"
                await context.storage_state(path=cookie_path)
                
                # Başarılı kayıt mühürü
                with open("basarili_pilotlar.txt", "a") as f:
                    f.write(f"{email_addr}:{password}\n")
                
                print(f"🍪 {email_addr} için session mühürlendi ve kaydedildi.")
                
            except Exception as e:
                # Hata anında kanıt alalım
                await page.screenshot(path="hata_kaniti.png")
                print(f"❌ Sorti başarısız: {str(e)[:70]}...")
            
            finally:
                # RAM sızıntısını önlemek için context'i her seferinde öldür
                await context.close()
                print("🔄 Sorti bitti, yeni tura geçiliyor...")

if __name__ == "__main__":
    try:
        asyncio.run(run_factory())
    except KeyboardInterrupt:
        print("\n🛑 Operasyon komutan tarafından durduruldu.")
