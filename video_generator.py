import json
import os
import random
import textwrap
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip

# --- AYARLAR ---
NEWS_FILE = "factory/trending_data.json"
VIDEO_DIR = "factory/raw_videos"
MUSIC_DIR = "factory/music"
OUTPUT_DIR = "factory/output_videos"
FONT_PATH = "assets/fonts/Montserrat-Bold.ttf"
LOGO_PATH = "assets/logo.png"  # Varsa logonu buraya atarsın

# TikTok Formatı
WIDTH = 1080
HEIGHT = 1920
DURATION = 10  # Her haber için süre

def wrap_text(text, width=20):
    return "\n".join(textwrap.wrap(text, width=width))

def create_videos():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    # 1. Haberleri Yükle
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    topics = data.get("raw_topics", [])
    hashtags = data.get("hashtags", [])

    if not topics:
        print("❌ Haber kaynağı boş! Önce trend_scraper.py çalıştır.")
        return

    # 2. Hammadde Kontrolü
    videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.mov'))]
    musics = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav'))]

    if not videos:
        print("❌ Hiç video yok! 'factory/raw_videos' klasörüne drone videosu at.")
        return

    print(f"🎬 FABRİKA BAŞLIYOR: {len(topics)} adet haber işlenecek...")

    # İlk 3 haberi video yapalım (Hepsini yaparsak sunucu şişebilir)
    for i, topic in enumerate(topics[:3]):
        try:
            print(f"🔨 İşleniyor ({i+1}): {topic[:30]}...")
            
            # --- VİDEO KATMANI ---
            video_path = os.path.join(VIDEO_DIR, random.choice(videos))
            clip = VideoFileClip(video_path)
            
            # Süreyi ayarla ve loopla (Eğer video kısaysa)
            if clip.duration < DURATION:
                clip = clip.loop(duration=DURATION)
            else:
                clip = clip.subclip(0, DURATION)
            
            # Dikey Crop (TikTok 9:16)
            # Videonun ortasından 1080x1920 kesit alır
            clip = clip.resize(height=1920) # Yüksekliği sabitle
            if clip.w > 1080:
                clip = clip.crop(x1=clip.w/2 - 540, y1=clip.h/2 - 960, width=1080, height=1920)
            
            # --- METİN KATMANI (BAŞLIK) ---
            # Beyaz yazı, siyah arka plan (Highlight effect)
            wrapped_title = wrap_text(topic.upper(), width=20)
            txt_clip = TextClip(
                wrapped_title, 
                font=FONT_PATH, 
                fontsize=70, 
                color='white', 
                bg_color='rgba(0,0,0,0.6)', # Yarı saydam siyah şerit
                method='caption',
                size=(900, None) # Genişliği sınırla
            ).set_position(('center', 'center')).set_duration(DURATION)

            # --- ALT METİN (HASHTAG) ---
            tag_text = hashtags[i] if i < len(hashtags) else "#Teknoloji"
            tag_clip = TextClip(
                tag_text, 
                font=FONT_PATH, 
                fontsize=40, 
                color='#00ffcc', # Neon yeşil
                bg_color='black'
            ).set_position(('center', 1600)).set_duration(DURATION)

            # --- LOGO KATMANI (Opsiyonel) ---
            layers = [clip, txt_clip, tag_clip]
            # Eğer logo dosyası varsa ekle
            if os.path.exists(LOGO_PATH):
                logo = (VideoFileClip(LOGO_PATH, has_mask=True)
                        .resize(height=150)
                        .set_position(("left", "top"))
                        .set_duration(DURATION))
                layers.append(logo)

            # --- SES KATMANI ---
            final_video = CompositeVideoClip(layers, size=(WIDTH, HEIGHT))
            
            if musics:
                music_path = os.path.join(MUSIC_DIR, random.choice(musics))
                music = AudioFileClip(music_path).subclip(0, DURATION).volumex(0.3) # Sesi kıs
                final_video = final_video.set_audio(music)

            # --- RENDER (ÇIKTI AL) ---
            output_filename = f"{OUTPUT_DIR}/video_{i}_{random.randint(1000,9999)}.mp4"
            final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac", fps=24, logger=None)
            
            print(f"✅ Video Hazır: {output_filename}")

        except Exception as e:
            print(f"❌ Hata ({topic[:10]}): {e}")

if __name__ == "__main__":
    create_videos()
