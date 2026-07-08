# Morphex-AI 🤖

**Türkçe Yapay Zeka Sohbet & Kod Asistanı**

Morphex-AI, Python ve Flask ile geliştirilmiş, yapay zeka destekli bir web uygulamasıdır. Kod yazma, kod inceleme, hata bulma ve genel sohbet yapabilir. Türkçe dil desteği ve Türkçe erkek sesi içerir.

## ✨ Özellikler

- 💬 **Sohbet:** Genel sorulara cevap veren AI
- 💻 **Kod Asistanı:** Kod yazma, inceleme, hata bulma
- 🔊 **Türkçe Ses:** Erkek sesi ile TTS
- 🔐 **Güvenli:** JWT token ile kimlik doğrulama
- 📱 **Responsive:** Mobil uyumlu tasarım
- 💾 **Geçmiş:** Konuşma kaydı ve depolama

## 🚀 Hızlı Başlama

### Gereksinimler
- Python 3.8+
- pip
- OpenAI API Key

### Kurulum
```bash
# Repository'yi klonla
git clone https://github.com/projeseven/Morphex-AI.git
cd Morphex-AI

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyası oluştur
echo "OPENAI_API_KEY=your_key_here" > .env

# Uygulamayı çalıştır
python app.py
```

Tarayıcında açı: **http://localhost:5000**

## 📚 Dokümantasyon

- [SETUP.md](SETUP.md) - Detaylı kurulum talimatları
- [FEATURES.md](FEATURES.md) - Özellikler ve gereksinimler
- [STRUCTURE.md](STRUCTURE.md) - Proje yapısı

## 🛠️ Stack

| Bileşen | Teknoloji |
|---------|-----------|
| Backend | Python + Flask |
| Frontend | HTML/CSS/JavaScript |
| Veritabanı | SQLite |
| AI | OpenAI API |
| Ses | pyttsx3 + gTTS |
| Kimlik Doğrulama | JWT |

## 📁 Klasör Yapısı

```
Morphex-AI/
├── app.py              # Ana aplikasyon
├── config.py           # Konfigürasyon
├── models.py           # Veritabanı modelleri
├── requirements.txt    # Bağımlılıklar
├── routes/             # API rotaları
│   ├── auth.py        # Kimlik doğrulama
│   ├── chat.py        # Sohbet API
│   └── code.py        # Kod işlemleri API
├── utils/              # Yardımcı modüller
│   ├── ai_service.py  # OpenAI entegrasyonu
│   └── tts.py         # Türkçe TTS
├── templates/          # HTML şablonları
│   ├── auth.html      # Giriş/Kayıt
│   └── chat.html      # Sohbet arayüzü
├── static/             # Statik dosyalar
│   ├── css/
│   │   └── style.css  # CSS stileri
│   └── js/
│       ├── auth.js    # Giriş JavaScript
│       └── chat.js    # Sohbet JavaScript
└── .env                # Ortam değişkenleri
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Yeni kullanıcı kaydı
- `POST /api/auth/login` - Giriş yapma
- `GET /api/auth/verify` - Token doğrulama

### Chat
- `POST /api/chat/send` - Mesaj gönder
- `GET /api/chat/history/<user_id>` - Sohbet geçmişi
- `POST /api/chat/speak` - Ses oluştur

### Code
- `POST /api/code/review` - Kod inceleme
- `POST /api/code/find-bugs` - Hata bulma
- `POST /api/code/write` - Kod yazma

## 🎯 Kullanım

1. **Kayıt Ol** - Yeni hesap oluştur
2. **Giriş Yap** - Hesabına giriş yap
3. **Sohbet Başlat** - 3 modu seç:
   - 💬 Sohbet: Genel sorular
   - 💻 Kod: Kod işlemleri
   - ❓ Soru: Bilgiye ulaş

## ⚙️ Konfigürasyon

`.env` dosyasında:
```
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key
OPENAI_API_KEY=your_openai_key
DEBUG=True  # Geliştirme ortamı için
```

## 🐛 Sorun Giderme

**Ses çalışmıyor?**
- Windows'ta Text-to-Speech açılı mı kontrol et
- Sistem sesinin açık olduğundan emin ol

**API Hatası?**
- OpenAI API key'i kontrol et
- İnternet bağlantısını kontrol et

**Port 5000 Kullanılıyor?**
```bash
python app.py --port 5001
```

## 📝 Lisans

Bu proje açık kaynaktır. Özgürce kullan ve geliştir!

## 👤 Geliştirici

**projeseven** - https://github.com/projeseven

## 🤝 Katkıda Bulun

Pull request'ler kabul edilir! Büyük değişiklikler için önce issue açın.

---

**⭐ Projeni beğendiysen yıldız ver!**
