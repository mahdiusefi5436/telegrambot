import os
import requests
import random
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

TOPICS = [
    "یه متن خیلی کوتاه و دلشکسته درباره شکست عشقی بنویس",
    "یه متن خیلی کوتاه و غمگین درباره تنهایی بنویس",
    "یه متن خیلی کوتاه و عاشقانه درباره دلتنگی بنویس",
    "یه متن خیلی کوتاه درباره خیانت بنویس",
    "یه متن خیلی کوتاه و فلسفی درباره زندگی بنویس",
    "یه متن خیلی کوتاه و طنز درباره روزمرگی بنویس",
    "یه متن خیلی کوتاه درباره دانشگاه و درس بنویس",
    "یه متن خیلی کوتاه و انگیزشی درباره موفقیت بنویس",
    "یه متن خیلی کوتاه درباره فراموشی و گذشته بنویس",
    "یه متن خیلی کوتاه و احساسی درباره عشق یک‌طرفه بنویس",
    "یه متن خیلی کوتاه و تلخ درباره جدایی بنویس",
    "یه متن خیلی کوتاه و امیدوارکننده درباره آینده بنویس",
    "یه متن خیلی کوتاه درباره دوستی و رفاقت بنویس",
    "یه متن خیلی کوتاه و طنز درباره پیشی و گربه بنویس",
    "یه متن خیلی کوتاه و فلسفی درباره ذهن و فکر بنویس",
]

def generate_post():
    topic = random.choice(TOPICS)
    
    prompt = f"""
    {topic}
    
    متن باید خیلی کوتاه باشه (حداکثر ۲ خط و کمتر از ۱۰۰ کاراکتر).
    احساسی و تأثیرگذار باشه.
    از یه ایموجی مناسب استفاده کن.
    فقط متن رو بنویس، توضیح اضافه نده.
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "تو یه نویسنده محتوای تلگرامی هستی که متن‌های خیلی کوتاه و احساسی می‌نویسی."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload)
    return r.status_code == 200

# اجرا
post = generate_post()
post += "\n\n📌 @Zaaban_English"

if send_to_telegram(post):
    print("✅ پست ارسال شد")
else:
    print("❌ خطا در ارسال")
