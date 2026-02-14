import json
import os

COOKIES_DIR = "cookies"
if not os.path.exists(COOKIES_DIR): os.makedirs(COOKIES_DIR)

print("1. Bilgisayarından TikTok'a gir.")
print("2. 'EditThisCookie' eklentisi ile cookie'leri kopyala (Export).")
print("3. O kopyaladığın JSON verisini aşağıya yapıştır ve ENTER'a bas.")
print("-" * 50)

raw_data = input("JSON VERİSİNİ YAPIŞTIR: ")

try:
    # Veriyi temizle ve JSON'a çevir
    cookie_data = json.loads(raw_data)
    
    # Dosyaya kaydet
    file_path = os.path.join(COOKIES_DIR, "manual_login.json")
    with open(file_path, "w") as f:
        json.dump({"cookies": cookie_data}, f) # Playwright formatına uyum
        
    print(f"\n✅ BAŞARILI! Cookie kaydedildi: {file_path}")
    print("Şimdi 'deploy_videos.py' dosyasını çalıştırabilirsin.")

except Exception as e:
    print(f"\n❌ HATA: Yapıştırdığın veri geçerli bir JSON değil! {e}")
