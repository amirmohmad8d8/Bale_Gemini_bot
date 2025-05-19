from flask import Flask, request
import requests

app = Flask(__name__)

BALE_TOKEN = 'توکن ربات بله'
GEMINI_API_KEY = 'کلید Gemini'
BALE_URL = f'https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage'
GEMINI_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']

    # ارسال پیام کاربر به Gemini
    gemini_response = requests.post(GEMINI_URL, json={
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    })

    if gemini_response.status_code == 200:
        reply_text = gemini_response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        reply_text = "متاسفم، مشکلی پیش اومد."

    # ارسال پاسخ به بله
    requests.post(BALE_URL, json={
        "chat_id": chat_id,
        "text": reply_text
    })

    return "ok"

if __name__ == '__main__':
    app.run(port=5000)