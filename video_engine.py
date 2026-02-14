import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import random

def get_tr_trends():
    print("📡 Türkiye gündemi çekiliyor...")
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=TR"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'xml')
        items = [item.title.text for item in soup.find_all('item')[:10]]
        print(f"✅ Gündem başlıkları alındı: {len(items)} tane.")
        return items
    except Exception as e:
        print(f"⚠️ Gündem çekilemedi: {e}")
        return ["Havacılık Tutkusu", "FPV Drone Life", "Teknoloji Gündemi"]

def create_unique_video(input_path, output_path, text):
    try:
        print(f"🎬 Video işleniyor: {input_path}")
        video = VideoFileClip(input_path)
        
        # Yazı katmanı
        txt_clip = TextClip(text, fontsize=50, color='white', font='Arial-Bold', 
                            method='caption', size=(video.w*0.8, None))
        txt_clip = txt_clip.set_pos('center').set_duration(video.duration)
        
        final_video = CompositeVideoClip([video, txt_clip])
        print(f"💾 Render başlatıldı: {output_path}")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, logger=None)
        
        video.close()
        final_video.close()
        return True
    except Exception as e:
        print(f"❌ Render Hatası: {e}")
        return False

if __name__ == "__main__":
    asset_path = "assets"
    asset_files = [f for f in os.listdir(asset_path) if f.lower().endswith(".mp4")]
    
    if not asset_files:
        print(f"🛑 HATA: '{asset_path}' klasöründe .mp4 dosya bulunamadı!")
        print("Lütfen assets içine birkaç ham video at aşkım.")
    else:
        trends = get_tr_trends()
        chosen_asset = os.path.join(asset_path, random.choice(asset_files))
        chosen_trend = random.choice(trends)
        output_name = f"output_videos/final_{random.randint(1000,9999)}.mp4"
        
        print(f"🔥 Operasyon Başladı | Gündem: {chosen_trend}")
        if create_unique_video(chosen_asset, output_name, chosen_trend):
            print(f"✨ BAŞARILI: {output_name} hazır!")
