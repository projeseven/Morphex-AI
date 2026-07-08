// ===== Auth JavaScript =====

// Tab Değiştir
function showTab(tabName) {
    // Tüm tab'ları gizle
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Tüm butonları pasif yap
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Seçili tab'ı göster
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Giriş Yap
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const messageDiv = document.getElementById('loginMessage');
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Token'ı localStorage'a kaydet
            localStorage.setItem('token', data.token);
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('username', data.username);
            
            messageDiv.className = 'message success';
            messageDiv.textContent = '✅ Başarıyla giriş yapıldı! Yönlendiriliyorsunuz...';
            
            setTimeout(() => {
                window.location.href = '/chat';
            }, 1500);
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = `❌ ${data.error}`;
        }
    } catch (error) {
        messageDiv.className = 'message error';
        messageDiv.textContent = `❌ Hata: ${error.message}`;
    }
});

// Kayıt Ol
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const passwordConfirm = document.getElementById('register-password-confirm').value;
    const messageDiv = document.getElementById('registerMessage');
    
    // Şifre kontrol
    if (password !== passwordConfirm) {
        messageDiv.className = 'message error';
        messageDiv.textContent = '❌ Şifreler eşleşmiyor!';
        return;
    }
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            messageDiv.className = 'message success';
            messageDiv.textContent = `✅ ${data.message} Giriş sekmesine geçebilirsiniz.`;
            
            // Formu temizle
            document.getElementById('registerForm').reset();
            
            // Giriş tabına geç
            setTimeout(() => {
                document.querySelector('.tab-btn').click();
            }, 2000);
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = `❌ ${data.error}`;
        }
    } catch (error) {
        messageDiv.className = 'message error';
        messageDiv.textContent = `❌ Hata: ${error.message}`;
    }
});
