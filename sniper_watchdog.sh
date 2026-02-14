#!/bin/bash
echo "🛡️ Sniper Watchdog Aktif Edildi!"
while true; do
    echo "🚀 [$(date +'%H:%M:%S')] Sniper göreve gönderiliyor..."
    # Sniper'ı çalıştırıyoruz
    python3 server_sniper.py
    # Eğer buraya gelirse sniper kapanmış demektir
    echo "⚠️ [$(date +'%H:%M:%S')] Sniper düştü! 10 saniye içinde yeniden diriltiliyor..."
    sleep 10
done
