from flask import Blueprint, request, jsonify
from models import db, Chat
import os

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/send', methods=['POST'])
def send_message():
    """Sohbet mesajı gönder"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        user_message = data.get('message')
        message_type = data.get('type', 'chat')  # 'chat', 'code', 'question'
        
        if not user_id or not user_message:
            return jsonify({'error': 'Kullanıcı ID veya mesaj eksik'}), 400
        
        # Yapay Zeka Cevabı (Şimdilik placeholder)
        ai_response = f"Türkçe cevap hazırlanıyor: {user_message}"
        
        # Sohbeti Veritabanına Kaydet
        chat = Chat(
            user_id=user_id,
            message_type=message_type,
            user_message=user_message,
            ai_response=ai_response
        )
        
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({
            'chat_id': chat.id,
            'user_message': user_message,
            'ai_response': ai_response,
            'message_type': message_type
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history/<int:user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Sohbet Geçmişini Al"""
    try:
        chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.desc()).all()
        
        history = [{
            'id': chat.id,
            'type': chat.message_type,
            'user_message': chat.user_message,
            'ai_response': chat.ai_response,
            'created_at': chat.created_at.isoformat()
        } for chat in chats]
        
        return jsonify({
            'user_id': user_id,
            'chat_count': len(history),
            'history': history
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
