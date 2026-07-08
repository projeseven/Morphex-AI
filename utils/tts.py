import pyttsx3
from gtts import gTTS
import os

class TurkishTTS:
    """Türkçe Text-to-Speech Sistemi"""
    
    def __init__(self):
        # pyttsx3 Engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Hız
        self.engine.setProperty('volume', 0.9)  # Ses Seviyesi
        
        # Türkçe Erkek Sesi Ayarla
        self.setup_voice()
    
    def setup_voice(self):
        """Türkçe Erkek Sesi Ayarla"""
        voices = self.engine.getProperty('voices')
        
        # Türkçe erkek sesi bul
        for voice in voices:
            if 'turkish' in voice.name.lower() or 'tr' in voice.id.lower():
                if 'male' in voice.name.lower() or 'boy' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
        
        # Fallback: İlk Türkçe sesi kullan
        for voice in voices:
            if 'tr' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                return
    
    def speak_local(self, text):
        """Lokal olarak ses çıkar (pyttsx3)"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Ses Hatası: {e}")
            return False
    
    def speak_to_file(self, text, filename='output.mp3'):
        """Sesi dosyaya kaydet (gTTS)"""
        try:
            tts = gTTS(text=text, lang='tr', slow=False)
            tts.save(filename)
            return True
        except Exception as e:
            print(f"Dosya Kayıt Hatası: {e}")
            return False
    
    def get_voice_file(self, text):
        """Ses dosyası URL'si oluştur"""
        try:
            tts = gTTS(text=text, lang='tr', slow=False)
            # Dosyaya kaydet
            filename = f"output_{hash(text)}.mp3"
            tts.save(filename)
            return filename
        except Exception as e:
            print(f"Hata: {e}")
            return None


# Global instance
tts_engine = TurkishTTS()

def speak(text):
    """Türkçe Ses Çıkart"""
    tts_engine.speak_local(text)

def save_speech(text, filename='speech.mp3'):
    """Türkçe Sesi Dosyaya Kaydet"""
    return tts_engine.speak_to_file(text, filename)
