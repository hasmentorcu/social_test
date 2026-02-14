import os
import random
import gc
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

GÜNDEM_LİSTESİ = [
    "Galatasaray - Eyüpspor", "Sevgililer Günü Mesajları", "Mauro Icardi", 
    "Panathinaikos - Fenerbahçe", "Kredi Kartı Limitleri Değişiyor", 
    "Trabzonspor - Fenerbahçe", "Süper Lig Gol Krallığı", "Arka Sokaklar 739. Bölüm",
    "Kızılcık Şerbeti 125. Bölüm", "Osimhen", "Teknofest 2026", "Donald Trump",
    "Merkez Bankası Faiz Kararı", "Antalyaspor - Samsunspor", "Hull City - Chelsea",
    "TRT1 Canlı İzle", "Rennes - PSG", "Orhan Pamuk Yeni Kitap", "Çorum - İstanbulspor",
    "Borussia Dortmund - Mainz 05", "Pisa - Milan", "Boluspor - Hatayspor", 
    "Zeynep Alkan", "Daca BBL", "Safiye Soyman", "Mersin Hava Durumu",
    "Nurseli İdiz", "Çağrı Hakan Balta", "Fransa 1. Ligi", "Eda Erdem",
    "TOD TV", "Süper Lig Maçları", "Rasim Arı", "İzmir Elektrik Kesintisi",
    "Teknoloji Gündemi", "God of War: Sons of Sparta", "ABD Enflasyon Verisi",
    "MSB Personel Temin", "Cuma Hutbesi Konusu", "Ankara Baraj Doluluk",
    "13 Şubat BİM Kataloğu 2026", "Ata Turizm Halka Arz", "Dilan Çıtak", "Yeni Trafik Cezaları"
]

def process_all_videos():
    asset_dir = "assets"
    output_dir = "output_videos"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    assets = [f for f in os.listdir(asset_dir) if f.lower().endswith(".mp4")]
    if not assets:
        print("🛑 HATA: Assets klasöründe video yok!")
        return

    print(f"🎬 Seri üretim (RAM Dostu Mod) başlıyor...")
    
    for i in range(1666):
        output_path = f"{output_dir}/final_pilot_{i+1}.mp4"
        if os.path.exists(output_path):
            continue
            
        asset = random.choice(assets)
        trend = random.choice(GÜNDEM_LİSTESİ)
        
        try:
            video = VideoFileClip(os.path.join(asset_dir, asset))
            duration = min(video.duration, 12)
            video = video.subclip(0, duration)
            
            txt = TextClip(trend, fontsize=60, color='yellow', font='Arial-Bold', 
                           stroke_color='black', stroke_width=2, method='caption', 
                           size=(video.w*0.9, None))
            txt = txt.set_pos('center').set_duration(video.duration)
            
            final = CompositeVideoClip([video, txt])
            
            # RAM koruması için threads=1 (veya 2) yapıyoruz
            final.write_videofile(output_path, codec="libx264", audio_codec="aac", 
                                  fps=24, logger=None, threads=1)
            
            print(f"✅ [{i+1}/1666] Üretildi: {trend}")
            
            # Bellek temizliği
            video.close()
            final.close()
            del video, final, txt
            gc.collect()
            
        except Exception as e:
            print(f"❌ Hata ({asset}): {e}")

if __name__ == "__main__":
    process_all_videos()
