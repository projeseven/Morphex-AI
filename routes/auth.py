from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import jwt
from datetime import datetime, timedelta
import os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'morphex-ai-secret-key-2026')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Yeni kullanıcı kaydı"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Eksik bilgi'}), 400
        
        # Kullanıcı zaten var mı kontrol et
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Kullanıcı adı zaten kullanılıyor'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email zaten kullanılıyor'}), 409
        
        # Yeni kullanıcı oluştur
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Başarıyla kayıt olundu',
            'user_id': user.id,
            'username': user.username
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Kullanıcı girişi"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Kullanıcı adı veya şifre eksik'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Geçersiz kullanıcı adı veya şifre'}), 401
        
        # JWT Token oluştur
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'message': 'Başarıyla giriş yapıldı',
            'token': token,
            'user_id': user.id,
            'username': user.username
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Token doğrulama"""
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token bulunamadı'}), 401
        
        token = token.replace('Bearer ', '')
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        
        if not user:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
        
        return jsonify({
            'valid': True,
            'user_id': user.id,
            'username': user.username
        }), 200
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token süresi dolmuş'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Geçersiz token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
