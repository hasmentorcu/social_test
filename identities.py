import random

# --- 1. MÜHİMMAT: İSİM HAVUZU (Yaklaşık 300 Popüler Türk Kadın İsmi) ---
# Bu liste çaprazlandığında on binlerce benzersiz sonuç üretir.
first_names = [
    "Zeynep", "Elif", "Defne", "Hande", "Aslı", "Merve", "Büşra", "Selin", "Esra", "Gamze",
    "İrem", "Kübra", "Aleyna", "Buse", "Yağmur", "Ece", "Derya", "Seda", "Gizem", "Nilay",
    "Deniz", "Pelin", "Simge", "Tuğçe", "Melis", "Ceren", "Ezgi", "Damla", "Beyza", "Şevval",
    "Rabia", "Sude", "Hilal", "Özge", "İlayda", "Dilan", "Gözde", "Burcu", "Hazal", "Cansu",
    "Meltem", "Sinem", "Ebru", "Didem", "Tuğba", "Duygu", "Sıla", "Eda", "Mine", "Neslihan",
    "Yasemin", "Aylin", "Beren", "Azra", "Nisan", "Eylül", "Doğa", "İpek", "Nazlı", "Melek",
    "Sena", "Zehra", "Fatma", "Ayşe", "Hatice", "Emine", "Sümeyye", "Şeyma", "Betül", "Feyza",
    "Rümeysa", "Esma", "Hafsa", "Zübeyde", "Hacer", "Meryem", "Asya", "Lina", "Ada", "Masal",
    "Öykü", "Berrin", "Nihan", "Bahar", "Arzu", "Sevgi", "Gül", "Lale", "Menekşe", "Yonca",
    "Sibel", "Demet", "Pınar", "Yeşim", "Gonca", "Filiz", "Nur", "Aysun", "Banu", "Canan",
    "Çağla", "Çiğdem", "Dilek", "Esin", "Funda", "Gülşah", "Hülya", "Irmak", "Jale", "Kader",
    "Leyla", "Müge", "Nalan", "Oya", "Pırıl", "Reyhan", "Sanem", "Şebnem", "Türkan", "Umay",
    "Vildan", "Yeliz", "Zerrin", "Ahu", "Bige", "Ceyda", "Dicle", "Ecem", "Fulya", "Gülce",
    "Handan", "Işıl", "Janset", "Kumru", "Leman", "Mina", "Nergis", "Oylum", "Parla", "Rengin",
    "Selda", "Şimal", "Tuana", "Utku", "Vuslat", "Yaren", "Zümrüt", "Alara", "Bade", "Cansın",
    "Derin", "Elgin", "Feray", "Gökçe", "Hayal", "Ilgar", "Kayra", "Lara", "Mira", "Nehir",
    "Okyanus", "Pamir", "Rüya", "Sahra", "Şira", "Tamay", "Ulya", "Verda", "Yosun", "Zeren",
    "Asmin", "Berfin", "Ceylan", "Delal", "Evin", "Hevi", "Jiyan", "Lorîn", "Mizgin", "Nupelda",
    "Rojda", "Şilan", "Zelal", "Armine", "Hermine", "Lerna", "Sibil", "Talin", "Zabel", "Eleni",
    "İrini", "Katerina", "Sofia", "Yorgo", "Zoi", "Alev", "Birsen", "Canel", "Devrim", "Eylem",
    "Fatoş", "Gülten", "Hasret", "İklim", "Jülide", "Kıymet", "Lütfiye", "Mukaddes", "Nuran",
    "Perihan", "Remziye", "Saadet", "Şükran", "Tenzile", "Ulviye", "Vahide", "Yüksel", "Zekiye",
    "Aybüke", "Bilge", "Çağrı", "Duru", "Gökçen", "Tomris", "Umay", "Selcan", "Banu", "Çiçek"
]

# --- 2. MÜHİMMAT: SOYİSİM HAVUZU (200 En Yaygın Soyisim) ---
last_names = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
    "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
    "Polat", "Korkmaz", "Özcan", "Çakır", "Erdoğan", "Yavuz", "Can", "Acar", "Şen", "Aktaş",
    "Güler", "Yalçın", "Güneş", "Bozkurt", "Bulut", "Keskin", "Ünal", "Turan", "Gül", "Özer",
    "Işık", "Kaplan", "Avcı", "Sarı", "Tekin", "Taş", "Köse", "Yüksel", "Ateş", "Aksoy",
    "Duran", "Türk", "Yücel", "Uysal", "Karakaş", "Çoşkun", "Eroğlu", "Mutlu", "Deniz", "Kocaman",
    "Gök", "Uçar", "Akyüz", "Kahraman", "Güven", "Sönmez", "İnce", "Erbil", "Karataş", "Metin",
    "Keleş", "Tunç", "Ay", "Dağ", "Akbulut", "Alkan", "Balcı", "Pek", "Toprak", "Bingöl",
    "Bayram", "Akkaya", "Bilgin", "Ekinci", "Adıgüzel", "Gündüz", "Apaydın", "Baştürk", "Duman",
    "Ergin", "Gürbüz", "Karaca", "Odabaş", "Sümer", "Taşkın", "Uzun", "Yaman", "Zengin", "Akın",
    "Barış", "Cengiz", "Durmaz", "Engin", "Fidan", "Genç", "Halis", "Ilgaz", "Kandemir", "Lale",
    "Mert", "Narin", "Oral", "Öz", "Pak", "Reis", "Sert", "Tamer", "Ulu", "Varol",
    "Yener", "Zorlu", "Akar", "Baş", "Canbaz", "Dinç", "Er", "Gedik", "Horasan", "İleri",
    "Kısa", "Limon", "Mumcu", "Nalbant", "Orak", "Öncel", "Pala", "Rüzgar", "Sancak", "Tan",
    "Usta", "Vural", "Yaşar", "Zeybek", "Akkuş", "Boz", "Ceylan", "Dindar", "Eser", "Gün",
    "Has", "İnal", "Karaduman", "Levent", "Mavi", "Nar", "Ozan", "Özlü", "Parlak", "Saka",
    "Şanlı", "Tanrıverdi", "Uğur", "Vatan", "Yazıcı", "Zafer", "Akbaş", "Bozan", "Coşar", "Diri",
    "Elmas", "Gümüş", "Haznedar", "İnan", "Karaman", "Lokman", "Mercan", "Nas", "Orhan", "Özmen",
    "Pehlivan", "Savaş", "Şeker", "Tanyeli", "Uluç", "Vardar", "Yazgan", "Zeren", "Akgül", "Bilir"
]

# --- 3. MÜHİMMAT: KAMUFLAJ BİO HAVUZU (Doğal, Bot Olmayan Sözler) ---
bios = [
    "Anı yakala ✨",
    "Kahve kokusu ve kitaplar ☕📚",
    "Hayat kısa, kuşlar uçuyor... 🕊️",
    "İstanbul 📍",
    "Gülümse, çekiyorum! 📸",
    "Kendi halinde biriyim 🌸",
    "Pozitif enerji ✨",
    "Müzik ruhun gıdasıdır 🎶",
    "Doğa aşığı 🌿",
    "Yeni yerler keşfetmeyi severim 🌍",
    "Moda ve tarz 👗",
    "Sadece huzur... ☁️",
    "Hayallerinin peşinden git 🚀",
    "Good vibes only ✌️",
    "Çay varsa umut var demektir ☕",
    "Deniz, kum, güneş ☀️",
    "Kediler ve ben 🐱",
    "Fotoğraf çekmeyi severim 📷",
    "Her şey güzel olacak 🌈",
    "Ankara / İstanbul ✈️",
    "Yazılım ve Teknoloji 💻",
    "Gamer Girl 🎮",
    "Netflix & Chill 🍿",
    "Spor ve Sağlıklı Yaşam 💪",
    "Burada yeniyim 👋",
    "DM kapalı 🚫",
    "Sadece eğlence için buradayım 🎉",
    "Mühendis 👷‍♀️",
    "Öğrenci 🎓",
    "Yemek yapmayı severim 🍳",
    "Sanat ve Tasarım 🎨",
    "Astroloji meraklısı ♈",
    "Kahve bağımlısı ☕",
    "Dünyayı gezmek istiyorum 🗺️",
    "Az insan çok huzur.",
    "Beni takip et 💖",
    "Yorum yapmayı unutma 👇",
    "Tiktok dünyasına giriş 🎬",
    "Sıradan bir gün 🌼",
    "Mutluluk bir seçimdir.",
    "Kendine inan ✨",
    "Asla pes etme!",
    "Günaydın dünya 🌞",
    "İyi geceler 🌙",
    "Hafta sonu modu on 🔛",
    "Pazartesi sendromu 😴",
    "Cuma neşesi 💃",
    "Yaz gelse de gitsek 🏖️",
    "Kış masalı ❄️",
    "Sonbahar hüznü 🍂",
    "İlkbahar çiçeği 🌷"
]

def get_random_identity():
    # 250 İsim * 200 Soyisim = 50.000 Benzersiz Kombinasyon
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    bio = random.choice(bios)
    return full_name, bio

# Test için (Bu dosya doğrudan çalıştırılırsa bir örnek basar)
if __name__ == "__main__":
    print(get_random_identity())
