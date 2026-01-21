from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

TELEGRAM_TOKEN = "8589389763:AAGECiVQ5kIibPaVlDFiV1_DvqH3mC9e3x0"

@app.route('/')
def home():
    return "🤖 Бот работает"

@app.route('/api/send-code', methods=['POST', 'OPTIONS'])
def send_code():
    # ВАЖНО: Обработка OPTIONS для CORS
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
        
        # Пробуем отправить в Telegram
        try:
            requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
                json={
                    'chat_id': username,
                    'text': f"🔐 Код: {code}",
                    'parse_mode': 'HTML'
                },
                timeout=3
            )
            telegram_sent = True
        except:
            telegram_sent = False
        
        response = jsonify({
            'success': True,
            'message': f'Код {code} принят',
            'telegram_sent': telegram_sent
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        response = jsonify({'success': False, 'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)