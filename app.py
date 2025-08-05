import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN', 'test_token_123')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'healthy',
        'service': 'Kazana Travel Bot',
        'timestamp': datetime.now().isoformat(),
        'webhook_token_set': bool(WEBHOOK_VERIFY_TOKEN),
        'whatsapp_token_set': bool(WHATSAPP_TOKEN)
    })

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return challenge, 200
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.get_json()
        logger.info(f"Received webhook data: {data}")
        return jsonify({'status': 'received'}), 200
    except Exception as e:
        logger.error(f"Webhook handling error: {e}")
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)