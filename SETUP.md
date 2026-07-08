# Başlangıç: Backend Kurulumu Tamamlandı ✅

## Adımlar:

### 1. Requirements Kur
```bash
pip install -r requirements.txt
```

### 2. Veritabanı Oluştur
```bash
python
>>> from app import create_app
>>> app = create_app()
>>> from models import db
>>> with app.app_context():
>>>     db.create_all()
```

### 3. Uygulamayı Başlat
```bash
python app.py
```

Sunucu şu adreste çalışacak: **http://localhost:5000**

## API Endpoints

### Kimlik Doğrulama
- `POST /api/auth/register` - Yeni kullanıcı kaydı
- `POST /api/auth/login` - Giriş yap
- `GET /api/auth/verify` - Token doğrula

### Sohbet
- `POST /api/chat/send` - Mesaj gönder
- `GET /api/chat/history/<user_id>` - Sohbet geçmişi

### Kod İşlemleri
- `POST /api/code/analyze` - Kod analizi
- `POST /api/code/review` - Kod inceleme
- `POST /api/code/save` - Kod kaydet

## Sonraki Adım
Frontend ve Ses Sistemi geliştireceğiz! 🚀
