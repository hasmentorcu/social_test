import requests
import os
import time

# --- AYARLAR ---
API_KEY = "hGodbUz8EPefHG4i0PNxcKsRRedWS4i7KL3JiMWSIPQD62M3DQQRmJOw"
QUERY = "FPV drone"
COUNT = 60
SAVE_DIR = "/root/TikTok-Account-Creator/TikTok-Account-Creator/assets"
# ---------------

def download_videos():
    headers = {"Authorization": API_KEY}
    # Portrait (dikey) videoları çekiyoruz
    url = f"https://api.pexels.com/videos/search?query={QUERY}&per_page={COUNT}&orientation=portrait"

    print(f"📡 Pexels'ten '{QUERY}' klipleri toplanıyor...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ Pexels Hatası: {response.status_code}")
            return

        data = response.json()
        videos = data.get("videos", [])
        print(f"✅ {len(videos)} tane dikey video mühürlendi. İndirme başlıyor...")

        for i, video in enumerate(videos):
            # En iyi dikey kaliteyi bulmaya çalışalım
            video_files = video.get("video_files", [])
            video_url = next((vf.get("link") for vf in video_files if vf.get("width") and vf.get("width") < vf.get("height")), None)
            
            if not video_url and video_files:
                video_url = video_files[0].get("link")

            if video_url:
                filename = os.path.join(SAVE_DIR, f"fpv_drone_{i+1}.mp4")
                print(f"📥 İndiriliyor ({i+1}/{len(videos)}): {filename}")
                v_res = requests.get(video_url, stream=True)
                with open(filename, 'wb') as f:
                    for chunk in v_res.iter_content(chunk_size=1024*1024):
                        if chunk: f.write(chunk)
                time.sleep(0.5) 
    except Exception as e:
        print(f"⚠️ Operasyon sırasında hata: {e}")

if __name__ == "__main__":
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    download_videos()
