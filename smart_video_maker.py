import json
import os
import random
import time
import requests
import gc
from playwright.sync_api import sync_playwright
from moviepy.editor import *
from moviepy.config import change_settings
from PIL import Image

# --- LINUX AYARLARI ---
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# --- DOSYA YOLLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "factory/trending_data.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "factory/output_videos")
MUSIC_DIR = os.path.join(BASE_DIR, "factory/music")
BG_MUSIC_PATH = os.path.join(MUSIC_DIR, "bg_music.mp3")
SYSTEM_FONT = "DejaVu-Sans-Bold"

# --- RAM TASARRUFU İÇİN AYARLAR ---
WIDTH = 720   # 1080 yerine 720p (Yarı yarıya RAM tasarrufu)
HEIGHT = 1280
DURATION = 6
FPS = 15      # 24 yerine 15 FPS

def resize_image_pil(img_path):
    """Resmi MoviePy'ye vermeden önce küçültür (RAM Tasarrufu)"""
    try:
        with Image.open(img_path) as img:
            img = img.convert('RGB')
            # En boy oranını koruyarak genişliği 800px yap (Yeterli)
            base_width = 800
            w_percent = (base_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_width, h_size), Image.LANCZOS)
            img.save(img_path) # Üzerine yaz
        return True
    except Exception as e:
        print(f"⚠️ Resim küçültme hatası: {e}")
        return False

def get_image_via_playwright(page, query):
    """Google Görseller'den Playwright ile resim avlar."""
    print(f"🔍 Görsel Aranıyor: {query}")
    try:
        search_url = f"https://www.google.com/search?q={query}&tbm=isch"
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)
        
        img_src = page.evaluate("""() => {
            const images = Array.from(document.querySelectorAll('img'));
            for (const img of images) {
                if (img.src.startsWith('http') && img.width > 150) {
                    return img.src;
                }
            }
            return null;
        }""")

        if not img_src: return None

        img_path = os.path.join(BASE_DIR, f"factory/temp_{random.randint(1000,9999)}.jpg")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(img_src, headers=headers, timeout=10)
        
        if response.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(response.content)
            return img_path
        return None
    except: return None

def create_smart_videos():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    has_music = os.path.exists(BG_MUSIC_PATH)
    if has_music: print(f"🎵 Müzik Hazır: {BG_MUSIC_PATH}")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    topics = data.get("raw_topics", [])

    print(f"🏭 AKILLI FABRİKA (LITE MODE) BAŞLIYOR: {len(topics)} konu...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()

        for i, topic in enumerate(topics[:5]): # İlk 5 test
            img_path = None
            final = None
            try:
                img_path = get_image_via_playwright(page, topic)
                if not img_path: continue

                # 1. RAM KORUMASI: Resmi önce küçült
                if not resize_image_pil(img_path): continue

                print(f"🔨 Montajlanıyor ({i+1}): {topic}")

                # 2. MoviePy İşlemleri
                original_img = ImageClip(img_path).set_duration(DURATION)
                
                # Arka Plan
                bg_clip = original_img.resize(height=HEIGHT)
                if bg_clip.w > WIDTH:
                    bg_clip = bg_clip.crop(x1=bg_clip.w/2 - WIDTH/2, width=WIDTH, height=HEIGHT)
                else:
                    bg_clip = bg_clip.resize(width=WIDTH)
                bg_clip = bg_clip.fl_image(lambda image: 0.3 * image)

                # Ön Plan (Zoom yok - RAM koruması)
                fg_clip = original_img.resize(width=WIDTH * 0.9).set_position("center")

                # Metin
                wrapped_txt = topic.upper()
                if len(wrapped_txt) > 20: wrapped_txt = wrapped_txt.replace(" ", "\n", 2)

                txt_clip = TextClip(
                    wrapped_txt,
                    font=SYSTEM_FONT,
                    fontsize=60,
                    color='white',
                    stroke_color='black',
                    stroke_width=2,
                    method='label',
                    size=(WIDTH*0.9, None)
                ).set_position('center').set_duration(DURATION)

                # Birleştir
                final = CompositeVideoClip([bg_clip, fg_clip, txt_clip], size=(WIDTH, HEIGHT))
                
                if has_music:
                    audio = AudioFileClip(BG_MUSIC_PATH)
                    if audio.duration < DURATION:
                        audio = audio.audio_loop(duration=DURATION)
                    else:
                        audio = audio.subclip(0, DURATION)
                    final = final.set_audio(audio)

                # RENDER (Optimized)
                safe_name = "".join([c for c in topic if c.isalnum() or c in " -_"]).replace(" ", "_")
                output_file = os.path.join(OUTPUT_DIR, f"video_{i}_{safe_name[:15]}.mp4")
                
                # threads=1 ve preset=ultrafast ÇOK ÖNEMLİ
                final.write_videofile(
                    output_file, 
                    fps=FPS, 
                    codec="libx264", 
                    audio_codec="aac", 
                    preset="ultrafast", 
                    threads=1, 
                    logger=None
                )
                print(f"✅ HAZIR: {output_file}")

            except Exception as e:
                print(f"❌ Hata ({topic}): {e}")
            
            finally:
                # TEMİZLİK (Garbage Collection)
                if final:
                    final.close()
                    del final
                if img_path and os.path.exists(img_path):
                    os.remove(img_path)
                gc.collect() # RAM'i zorla boşalt
        
        browser.close()

if __name__ == "__main__":
    create_smart_videos()
