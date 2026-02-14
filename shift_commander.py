import time
from datetime import datetime
import subprocess
import os

# --- AYARLAR ---
CREATOR_SCRIPT = "server_sniper.py" 
HARVESTER_SCRIPT = "cookie_harvester.py"
THREAD_COUNT = "10" # Burayı sunucu gücüne göre değiştirebilirsin

def run_script(script_name, inputs=None):
    print(f"🚀 [{datetime.now().strftime('%H:%M')}] {script_name} başlatılıyor...")
    # Script input bekliyorsa (Thread sayısı gibi), echo ile gönderiyoruz
    cmd = f"echo '{inputs}' | python3 {script_name}" if inputs else f"python3 {script_name}"
    
    process = subprocess.Popen(
        cmd, 
        shell=True,
        stdout=open("script_output.log", "a"),
        stderr=subprocess.STDOUT
    )
    return process

def main():
    print("🎖️ VARDİYA KOMUTANI (V3-SNIPER) DEVREDE!")
    ac_proc = None
    hv_proc = None

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # 1. HESAP OLUŞTURMA VARDİYASI (Şu an - 21:30)
        if "00:00" <= current_time < "21:30":
            if ac_proc is None or ac_proc.poll() is not None:
                print("⚒️ SERVER SNIPER VARDİYASI BAŞLADI!")
                ac_proc = run_script(CREATOR_SCRIPT, inputs=THREAD_COUNT)
        
        # 2. COOKIE TOPLAMA VARDİYASI (21:30 - 01:00)
        elif "21:30" <= current_time < "01:00":
            if ac_proc:
                print("🛑 Sniper durduruluyor, Harvester sırası...")
                ac_proc.terminate()
                ac_proc = None
            
            if hv_proc is None or hv_proc.poll() is not None:
                print("🍪 HARVESTER VARDİYASI BAŞLADI!")
                hv_proc = run_script(HARVESTER_SCRIPT)

        time.sleep(60)

if __name__ == "__main__":
    main()
