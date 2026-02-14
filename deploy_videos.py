import os
import random
import time
import shutil
from playwright.sync_api import sync_playwright

# --- AYARLAR ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "factory/output_videos")
ARCHIVE_DIR = os.path.join(BASE_DIR, "factory/archive")
COOKIES_DIR = os.path.join(BASE_DIR, "cookies")

# Daha sade bir URL deneyelim
UPLOAD_URL = "https://www.tiktok.com/upload?lang=en"

def get_caption_from_filename(filename):
    try:
        clean_name = filename.split("_", 2)[2].replace(".mp4", "").replace("_", " ")
        return f"{clean_name} #fyp #kesfet #viral #tiktok"
    except:
        return "Viral Video #fyp"

def upload_videos():
    if not os.path.exists(ARCHIVE_DIR): os.makedirs(ARCHIVE_DIR)
    videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
    if not videos: return print("❌ Video yok.")
    cookie_files = [f for f in os.listdir(COOKIES_DIR) if f.endswith(".json")]
    if not cookie_files: return print("❌ Cookie yok.")

    print(f"🕵️ TEŞHİS VE YÜKLEME MODU: {len(videos)} video...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, # Sunucuda olduğumuz için True
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        for video_file in videos:
            print(f"\n🎬 İŞLENİYOR: {video_file}")
            cookie_path = os.path.join(COOKIES_DIR, random.choice(cookie_files))
            
            context = browser.new_context(
                storage_state=cookie_path,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            try:
                print("🌍 Sayfaya gidiliyor...")
                page.goto(UPLOAD_URL, timeout=60000)
                
                # Sayfanın iyice oturmasını bekle
                time.sleep(10)
                
                # --- TEŞHİS RAPORU ---
                title = page.title()
                url = page.url
                content_preview = page.inner_text("body")[:200].replace("\n", " ")
                
                print(f"📊 RAPOR:")
                print(f"   🔗 URL: {url}")
                print(f"   📑 Başlık: {title}")
                print(f"   👀 Görünen İlk Metin: {content_preview}...")
                
                # Hata Kontrolleri
                if "login" in url or "Log in" in title:
                    print("❌ HATA: Giriş sayfasına yönlendirildi. Cookie geçersiz!")
                    continue
                if "captcha" in content_preview.lower() or "verify" in content_preview.lower():
                    print("❌ HATA: Captcha/Doğrulama çıktı!")
                    continue

                # YÜKLEME DENEMESİ (Iframe ve Ana Sayfa Taraması)
                print("📥 Yükleme alanı aranıyor...")
                
                # Olası tüm 'Dosya Seç' butonları
                targets = [
                    page.frame_locator('iframe[src*="creator"]').locator('input[type="file"]'), # Iframe içi input
                    page.locator('input[type="file"]'), # Ana sayfa input
                    page.frame_locator('iframe[src*="creator"]').locator('button:has-text("Select file")'), # Iframe içi buton
                    page.locator('button:has-text("Select file")'), # Ana sayfa buton
                    page.locator('div[aria-label="Select file"]') # Div buton
                ]

                found_element = None
                for t in targets:
                    if t.count() > 0:
                        found_element = t
                        print(f"✅ Hedef bulundu: {t}")
                        break
                
                if found_element:
                    # Input ise direkt yükle, Buton ise tıkla
                    tag_name = found_element.evaluate("el => el.tagName")
                    if tag_name == "INPUT":
                        found_element.set_input_files(os.path.join(VIDEO_DIR, video_file))
                    else:
                        with page.expect_file_chooser() as fc_info:
                            found_element.click()
                        fc_info.value.set_files(os.path.join(VIDEO_DIR, video_file))
                    
                    print("📦 Dosya gönderildi! Yükleme bekleniyor...")
                    time.sleep(20)

                    # Başlık ve Paylaşım...
                    caption = get_caption_from_filename(video_file)
                    
                    # Editör bulma
                    editor = page.locator('.public-DraftEditor-content')
                    if editor.count() == 0: editor = page.frame_locator('iframe[src*="creator"]').locator('.public-DraftEditor-content')
                    
                    if editor.count() > 0:
                        editor.click()
                        time.sleep(1)
                        editor.type(caption)
                        print("✍️ Başlık yazıldı.")
                    
                    # Paylaş butonu
                    post_btn = page.locator('button:has-text("Post")')
                    if post_btn.count() == 0: post_btn = page.frame_locator('iframe[src*="creator"]').locator('button:has-text("Post")')
                    
                    if post_btn.count() > 0 and post_btn.is_enabled():
                        post_btn.click()
                        print("🚀 Paylaş butonuna basıldı!")
                        time.sleep(15)
                        shutil.move(os.path.join(VIDEO_DIR, video_file), os.path.join(ARCHIVE_DIR, video_file))
                        print(f"🎉 İŞLEM TAMAM: {video_file}")
                    else:
                        print("❌ Paylaş butonu aktif değil veya bulunamadı.")

                else:
                    print("❌ KRİTİK: Hiçbir yükleme butonu bulunamadı.")
                    # Sayfanın ekran görüntüsünü alalım ki görebilelim
                    page.screenshot(path="factory/debug_page.png")

            except Exception as e:
                print(f"❌ HATA: {e}")

            finally:
                context.close()
        browser.close()

if __name__ == "__main__":
    upload_videos()
