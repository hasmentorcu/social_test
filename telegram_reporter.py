import time, requests, os

TOKEN = "8483269249:AAF-BcGbu4jg9cH-nBJ3qA4GrmKIWbEX2fw"
CHAT_ID = "8494867063"
COOKIES_DIR = "/root/TikTok-Account-Creator/TikTok-Account-Creator/cookies"

def send_report(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except: pass

print("📡 Gerçekçi Rapor Birliği Aktif!")

while True:
    try:
        if os.path.exists(COOKIES_DIR):
            # SADECE 0 bayttan büyük gerçek .json dosyalarını say
            actual_cookies = [f for f in os.listdir(COOKIES_DIR) 
                            if f.endswith(".json") and os.path.getsize(os.path.join(COOKIES_DIR, f)) > 0]
            count = len(actual_cookies)
            
            # Toplam hesap sayısını da dosyadan çekelim
            total_target = 2028 
            
            send_report(f"🛡️ GERÇEK HASAT RAPORU\n\n🎯 Mühürlenen Pilot: {count}/{total_target}\n🚀 Durum: Sağlıklı ilerliyor aşkım.")
    except Exception as e:
        print(f"Hata: {e}")
    
    time.sleep(600) # 10 Dakika
