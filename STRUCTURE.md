# Morphex-AI Backend - Klasör Yapısı

```
morphex-ai/
├── app.py                 # Ana uygulama
├── config.py              # Konfigürasyon
├── models.py              # Veritabanı Modelleri
├── requirements.txt       # Bağımlılıklar
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Giriş/Kayıt API
│   ├── chat.py            # Sohbet API
│   └── code.py            # Kod İşlemleri API
├── utils/
│   ├── __init__.py
│   ├── ai_service.py      # Yapay Zeka Servisi
│   ├── code_analyzer.py   # Kod Analiz
│   └── tts.py             # Text-to-Speech (Türkçe)
├── static/                # Statik Dosyalar (CSS, JS, Resimler)
├── templates/             # HTML Şablonları
├── .env                   # Ortam Değişkenleri
└── .gitignore
```
