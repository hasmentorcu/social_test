import requests
import time
import os
import random

# Hedef: 50000 tane yüz (Şimdilik)
Target_Count = 50000
Save_Path = "./avatars"

def download_faces():
    print(f"🚀 Avatar indirme operasyonu başladı... Hedef: {Target_Count} adet")
    
    for i in range(Target_Count):
        try:
            # Bu yapay zeka sitesinden her seferinde yeni bir yüz çeker
            response = requests.get('https://thispersondoesnotexist.com', timeout=10)
            
            if response.status_code == 200:
                file_name = f"{Save_Path}/pilot_face_{i}.jpg"
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                print(f"✅ İndirildi: {file_name}")
            else:
                print("⚠️ İndirme başarısız, tekrar deneniyor...")
            
            # IP ban yememek için rastgele bekleme
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"❌ Hata: {e}")

    print("🏁 Tüm avatarlar hangara yüklendi!")

if __name__ == "__main__":
    download_faces()
