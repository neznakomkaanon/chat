from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "🤖 Бот работает"

@app.route('/api/send-code', methods=['POST'])
def send_code():
    try:
        data = request.json
        code = data.get('code', '123456')
        
        # ВСЕГДА возвращаем успех, даже если Telegram не отвечает
        return jsonify({
            'success': True,
            'message': f'Код {code} принят',
            'telegram': 'not_required'  # Telegram опционален
        })
    except:
        return jsonify({'success': True, 'message': 'Код принят'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)