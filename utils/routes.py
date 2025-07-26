import json
import os
import requests
from flask import jsonify

def handle_whatsapp(request):
    try:
        data = request.get_json()
        print("Received WhatsApp message:", json.dumps(data, indent=2))

        if 'entry' not in data:
            return jsonify(status="no_entry"), 200

        for entry in data['entry']:
            for change in entry.get('changes', []):
                if change['field'] != 'messages':
                    continue

                value = change['value']

                if 'statuses' in value:
                    print("Status update received")
                    continue

                for message in value.get('messages', []):
                    process_message(message, value)
        return jsonify(status="received"), 200

    except Exception as e:
        print(f"Error handling WhatsApp webhook: {e}")
        return jsonify(status="error", message=str(e)), 500

def process_message(message, value):
    try:
        from_number = message.get('from')
        msg_text = message.get('text', {}).get('body', '').lower().strip()

        reply = generate_reply(msg_text)
        send_whatsapp_message(from_number, reply)

    except Exception as e:
        print(f"Error processing message: {e}")

def generate_reply(user_input):
    if 'hello' in user_input or 'hi' in user_input:
        return "👋 Hello from Kazana! Ask me about travel routes, fares, or booking help."
    elif 'book' in user_input:
        return "📲 To book a seat, reply with: BOOK [Route] [Date]"
    elif 'route' in user_input:
        return "🛣️ Example Route: Harare ↔ Bulawayo | Express: $18, Economy: $12"
    return "🤖 I can help with travel info, booking, and fares. Just ask!"

def send_whatsapp_message(to_number, message):
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('PHONE_NUMBER_ID')

    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": message}
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"WhatsApp API Response: {response.status_code} - {response.text}")
