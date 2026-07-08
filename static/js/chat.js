// ===== Chat JavaScript =====

let currentMode = 'chat';
let token = localStorage.getItem('token');
let userId = localStorage.getItem('user_id');

// Token kontrol
if (!token) {
    window.location.href = '/';
}

// Mode Değiştir
function switchMode(mode) {
    currentMode = mode;
    
    // Butonları güncelle
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Başlığı güncelle
    const titles = {
        'chat': '💬 Sohbet',
        'code': '💻 Kod Asistanı',
        'question': '❓ Sorular'
    };
    document.getElementById('modeTitle').textContent = titles[mode];
    
    // Mesajları temizle
    document.getElementById('chatMessages').innerHTML = `
        <div class="system-message">
            ${mode === 'chat' ? '💬 Sohbet moduna hoş geldiniz!' : ''}
            ${mode === 'code' ? '💻 Kod yazma, inceleme ve hata bulma moduna hoş geldiniz!' : ''}
            ${mode === 'question' ? '❓ Soru sorma moduna hoş geldiniz!' : ''}
        </div>
    `;
}

// Mesaj Gönder
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Kullanıcı mesajını göster
    addMessageToChat('user', message);
    input.value = '';
    
    try {
        const response = await fetch('/api/chat/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                user_id: userId,
                message: message,
                type: currentMode
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // AI cevabını göster
            addMessageToChat('ai', data.ai_response);
            
            // Ses ile oku (Türkçe)
            speakText(data.ai_response);
        } else {
            addMessageToChat('ai', `❌ Hata: ${data.error}`);
        }
    } catch (error) {
        addMessageToChat('ai', `❌ Bağlantı hatası: ${error.message}`);
    }
}

// Mesajı Chat'e Ekle
function addMessageToChat(sender, text) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Eğer sistem mesajı varsa, silebilir
    const systemMsg = chatMessages.querySelector('.system-message');
    if (systemMsg) {
        systemMsg.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-item ${sender}`;
    messageDiv.innerHTML = `
        <div class="message-bubble">${escapeHtml(text)}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// HTML Escape (Güvenlik)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Türkçe Ses ile Oku
function speakText(text) {
    // Web Speech API kullan
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Türkçe dil ayarla
        utterance.lang = 'tr-TR';
        
        // Erkek sesi bulmaya çalış
        const voices = speechSynthesis.getVoices();
        const turkishMaleVoice = voices.find(voice => 
            voice.lang === 'tr-TR' && voice.name.includes('Male')
        );
        
        if (turkishMaleVoice) {
            utterance.voice = turkishMaleVoice;
        } else {
            // Fallback olarak Türkçe ses
            const turkishVoice = voices.find(voice => voice.lang === 'tr-TR');
            if (turkishVoice) {
                utterance.voice = turkishVoice;
            }
        }
        
        utterance.rate = 1;
        utterance.pitch = 1;
        
        speechSynthesis.speak(utterance);
    }
}

// Ses Kontrolü Değiştir
let voiceEnabled = false;
function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    const btn = document.querySelector('.btn-icon');
    btn.textContent = voiceEnabled ? '🔊' : '🔇';
}

// Ses İnputu Başlat (Microphone)
function startVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Tarayıcınız Ses İnputu desteklemiyor!');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.lang = 'tr-TR';
    recognition.interimResults = true;
    
    recognition.onstart = () => {
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.style.background = '#ff6b6b';
        voiceBtn.textContent = '🎤 Dinleniyor...';
    };
    
    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        document.getElementById('messageInput').value = transcript;
    };
    
    recognition.onend = () => {
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.style.background = '#f0f0f0';
        voiceBtn.textContent = '🎤';
    };
    
    recognition.start();
}

// Enter tuşu ile mesaj gönder
document.getElementById('messageInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Çıkış Yap
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    window.location.href = '/';
}

// Sohbet Geçmişini Yükle (Başlangıçta)
async function loadChatHistory() {
    try {
        const response = await fetch(`/api/chat/history/${userId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            // Son 10 mesajı göster
            data.history.slice(-10).reverse().forEach(chat => {
                addMessageToChat('user', chat.user_message);
                addMessageToChat('ai', chat.ai_response);
            });
        }
    } catch (error) {
        console.error('Geçmiş yükleme hatası:', error);
    }
}

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
});
