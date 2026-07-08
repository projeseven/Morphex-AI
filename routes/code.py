from flask import Blueprint, request, jsonify
from models import db, CodeSnippet
import re

code_bp = Blueprint('code', __name__)

@code_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """Kod Analizi Yap"""
    try:
        data = request.get_json()
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Kod eksik'}), 400
        
        # Basit Kod Analizi
        analysis = {
            'lines': len(code.split('\n')),
            'has_errors': check_code_errors(code),
            'suggestions': get_suggestions(code, language)
        }
        
        return jsonify(analysis), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@code_bp.route('/review', methods=['POST'])
def review_code():
    """Kod İncele"""
    try:
        data = request.get_json()
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Kod eksik'}), 400
        
        review = {
            'quality_score': calculate_quality_score(code),
            'issues': find_code_issues(code),
            'improvements': get_improvements(code)
        }
        
        return jsonify(review), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@code_bp.route('/save', methods=['POST'])
def save_code():
    """Kod Kaydet"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        title = data.get('title')
        code = data.get('code')
        language = data.get('language', 'python')
        
        if not all([user_id, title, code]):
            return jsonify({'error': 'Eksik bilgi'}), 400
        
        snippet = CodeSnippet(
            user_id=user_id,
            title=title,
            code=code,
            language=language
        )
        
        db.session.add(snippet)
        db.session.commit()
        
        return jsonify({
            'id': snippet.id,
            'title': title,
            'message': 'Kod başarıyla kaydedildi'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Yardımcı Fonksiyonlar
def check_code_errors(code):
    """Kod hatalarını kontrol et"""
    errors = []
    
    # Basit hata kontrolleri
    if code.count('(') != code.count(')'):
        errors.append('Parantez sayısı eşit değil')
    if code.count('[') != code.count(']'):
        errors.append('Köşeli parantez sayısı eşit değil')
    if code.count('{') != code.count('}'):
        errors.append('Küme parantez sayısı eşit değil')
    
    return errors

def get_suggestions(code, language):
    """Kod önerileri"""
    suggestions = []
    
    if language == 'python':
        if 'import *' in code:
            suggestions.append('Wildcard import kullanmaktan kaçının')
        if code.count('  ') > code.count('\t'):
            suggestions.append('Tutarlı indentation kullanın')
    
    return suggestions

def calculate_quality_score(code):
    """Kod kalite puanı hesapla (0-100)"""
    score = 100
    
    # Hatalar için puan kıs
    errors = check_code_errors(code)
    score -= len(errors) * 10
    
    # Boş satırlar için puan kıs
    if len(code.split('\n')) > 100:
        score -= 5
    
    return max(0, score)

def find_code_issues(code):
    """Kod sorunlarını bul"""
    issues = []
    
    if 'TODO' in code or 'FIXME' in code:
        issues.append('TODO/FIXME yorumları var')
    if len(code) > 5000:
        issues.append('Kod çok uzun, modüllere bölebilirsiniz')
    
    return issues

def get_improvements(code):
    """İyileştirme önerileri"""
    improvements = []
    improvements.append('Kod yorumları ekleyin')
    improvements.append('Fonksiyon isimleri daha açıklayıcı olabilir')
    
    return improvements
