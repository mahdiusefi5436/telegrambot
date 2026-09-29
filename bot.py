import os
import requests
import random
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["8934519828:AAG5KlRqjIqXHYxbTQPQySw0M_-oePjAsBE"]
CHANNEL_ID = os.environ["-1003597498641"]
DEEPSEEK_KEY = os.environ["sk-eb8a7d32e99443eda88c7e596c7d415d"]

client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

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
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "تو یه نویسنده محتوای تلگرامی هستی. متن‌های کوتاه، احساسی و تأثیرگذار بنویس. از ایموجی‌های مناسب استفاده کن."},
        {"role": "user", "content": selected}
    ]
)

text = response.choices[0].message.content

# اضافه کردن آیدی کانال به آخر متن
text += "\n\n📌 @testbotml"

# ارسال به کانال
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
