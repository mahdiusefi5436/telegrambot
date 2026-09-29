import os
import requests
import random
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

topics = [
    "یه بیوگرافی کوتاه و دلشکسته بنویس، پر از حس تنهایی و غم",
    "یه بیوگرافی کوتاه و غمگین بنویس، انگار کسی رو از دست دادی",
    "یه بیوگرافی کوتاه و عاشقانه بنویس، پر از حس دلتنگی",
    "یه بیوگرافی کوتاه درباره خیانت بنویس، پر از حس شکست و بی‌اعتمادی",
    "یه متن کوتاه و غمگین عاشقانه بنویس، انگار عشقت رفته",
    "یه بیوگرافی کوتاه درباره دلشکستگی بنویس، آروم و پر از درد",
    "یه متن کوتاه درباره خیانت عاشقانه بنویس، تلخ و واقعی"
]

selected = random.choice(topics)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "تو یه نویسنده محتوای تلگرامی هستی. متن‌های کوتاه، احساسی و تأثیرگذار بنویس. از ایموجی‌های مناسب استفاده کن."},
        {"role": "user", "content": selected}
    ]
)

text = response.choices[0].message.content
text += "\n\n📌 @testbotml"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
# test
