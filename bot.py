from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

print("🚀 Бот запускается...")

app = Flask(__name__)
CORS(app)  # ← ВАЖНО: разрешаем все CORS запросы

TELEGRAM_TOKEN = "8589389763:AAGECiVQ5kIibPaVlDFiV1_DvqH3mC9e3x0"

print("✅ Flask инициализирован с CORS")

@app.route('/')
def home():
    return "🤖 API для Незнакомки работает!"

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'neznakomka-bot'})

@app.route('/api/send-code', methods=['POST', 'OPTIONS'])
def send_code():
    # Обработка preflight запросов
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.json
        username = data.get('username', '').replace('@', '')
        code = data.get('code', '')
        
        if not username or not code:
            return jsonify({'success': False, 'error': 'Missing data'}), 400
        
        print(f"📨 Отправляем код {code} пользователю @{username}")
        
        # Отправляем через Telegram API
        response = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            json={
                'chat_id': username,
                'text': f"🔐 Код подтверждения для Незнакомки: {code}\n\nВведите этот код на сайте для входа в анонимный чат.\n\nКод действителен 10 минут.",
                'parse_mode': 'HTML'
            },
            timeout=10
        )
        
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Код отправлен @{username}")
            response = jsonify({'success': True})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            error_msg = result.get('description', 'Unknown error')
            print(f"❌ Ошибка отправки @{username}: {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 400
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Запускаем сервер на порту {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)