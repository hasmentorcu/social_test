import requests
import xml.etree.ElementTree as ET
import json
import os
import re

# --- AYARLAR ---
# Hedef: Sadece Teknoloji ve Bilim Haberleri (Siyaset ve 3. Sayfa haberleri engellendi)
RSS_SOURCES = [
    "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?ceid=TR:tr&hl=tr&gl=TR", # Teknoloji
    "https://news.google.com/rss/headlines/section/topic/SCIENCE?ceid=TR:tr&hl=tr&gl=TR"     # Bilim & Uzay
]
OUTPUT_FILE = "factory/trending_data.json"

# ⛔ DEMİR KUBBE: Bu kelimeleri içeren hiçbir haberi alma
BANNED_KEYWORDS = [
    "siyaset", "parti", "cumhurbaşkanı", "başkan", "bakan", "chp", "akp", "mhp", "dem",
    "tecavüz", "taciz", "cinayet", "ölüm", "yaralı", "şehit", "terör", "fetö", "pkk", "deaş",
    "uyuşturucu", "gözaltı", "hapis", "tutuklama", "kavga", "silah", "bıçak", "maganda",
    "dolandırıcı", "hırsız", "intihar", "kaza", "enkaz", "deprem", "yangın", "felaket",
    "boşanma", "nafaka", "aldatma", "magazin", "ünlü", "frikik", "bikinili"
]

def clean_hashtag(text):
    # Türkçe karakterleri temizle
    mapping = {'ğ': 'g', 'ü': 'u', 'ş': 's', 'ı': 'i', 'ö': 'o', 'ç': 'c', 
               'Ğ': 'G', 'Ü': 'U', 'Ş': 'S', 'İ': 'I', 'Ö': 'O', 'Ç': 'C'}
    for k, v in mapping.items():
        text = text.replace(k, v)
    
    # Sadece harf ve rakamları bırak
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    return f"#{text}"

def is_safe(title):
    title_lower = title.lower()
    for ban in BANNED_KEYWORDS:
        if ban in title_lower:
            return False
    return True

def fetch_safe_trends():
    print(f"🛡️ GÜVENLİ MOD: Teknoloji ve Bilim İstihbaratı Başlıyor...")
    
    intel_data = {
        "source": "Google Tech & Science",
        "hashtags": [],
        "raw_topics": []
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Compatible; TechBot/1.0)'}

    for url in RSS_SOURCES:
        try:
            print(f"🔗 Taranıyor: {url.split('topic/')[1].split('?')[0]}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                count = 0
                
                for item in root.iter('item'):
                    title = item.find('title').text
                    
                    # Kaynak ismini temizle (Örn: " - ShiftDelete.Net")
                    if "-" in title:
                        title = title.rsplit("-", 1)[0].strip()

                    # 🔍 GÜVENLİK KONTROLÜ
                    if not is_safe(title):
                        print(f"🚫 Engellendi (Güvenli Değil): {title[:40]}...")
                        continue

                    # Hashtag çok uzunsa kırp (TikTok algoritması kısa tag sever)
                    hashtag = clean_hashtag(title)
                    if len(hashtag) > 50: 
                        hashtag = hashtag[:50] # Çok uzun tagleri kes

                    intel_data["raw_topics"].append(title)
                    intel_data["hashtags"].append(hashtag)
                    
                    print(f"✅ Onaylandı: {title[:40]}... -> {hashtag}")
                    
                    count += 1
                    if count >= 8: break # Her kategoriden 8 haber al
                
        except Exception as e:
            print(f"❌ Hata: {e}")

    # Sonuçları Kaydet
    if intel_data["hashtags"]:
        if not os.path.exists("factory"): os.makedirs("factory")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(intel_data, f, ensure_ascii=False, indent=4)
        print(f"\n💾 DEPOLANDI: {len(intel_data['hashtags'])} adet 'Marka Dostu' haber yakalandı.")
    else:
        print("\n⚠️ Uygun haber bulunamadı.")

if __name__ == "__main__":
    fetch_safe_trends()
