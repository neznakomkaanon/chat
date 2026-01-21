from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

@app.route('/')
def home():
    return "🤖 Бот работает"

@app.route('/api/send-code', methods=['POST', 'OPTIONS'])
def send_code():
    # Обработка OPTIONS запроса
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
    
    try:
        data = request.json
        code = data.get('code', '123456')
        
        return jsonify({
            'success': True,
            'message': f'Код {code} принят'
        })
    except:
        return jsonify({'success': True, 'message': 'Код принят'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)