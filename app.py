from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import config
from models import db
from datetime import datetime

def create_app(config_name='development'):
    """Flask Uygulaması Oluştur"""
    
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Konfigürasyon Yükle
    app.config.from_object(config[config_name])
    
    # Veritabanı İnit
    db.init_app(app)
    
    # CORS Aktif Et
    CORS(app)
    
    # Blueprint'leri Kayıt Et
    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.code import code_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(code_bp, url_prefix='/api/code')
    
    # Frontend Routes
    @app.route('/', methods=['GET'])
    def index():
        """Ana Sayfa - Giriş/Kayıt"""
        return render_template('auth.html')
    
    @app.route('/chat', methods=['GET'])
    def chat():
        """Sohbet Sayfası"""
        return render_template('chat.html')
    
    # Hata İşleme
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Sayfa Bulunamadı'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Sunucu Hatası'}), 500
    
    # Başlangıç Route'u
    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({
            'status': 'ok',
            'message': 'Morphex-AI Backend Çalışıyor',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    # Veritabanı Context
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
