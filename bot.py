import os
import requests
import random
import time
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# موضوعات آموزشی
TOPICS = [
    "یه جمله انگلیسی درباره زندگی روزمره بنویس",
    "یه جمله انگلیسی درباره کار و شغل بنویس",
    "یه جمله انگلیسی درباره سفر بنویس",
    "یه جمله انگلیسی درباره غذا و رستوران بنویس",
    "یه جمله انگلیسی درباره خرید کردن بنویس",
    "یه جمله انگلیسی درباره خانواده بنویس",
    "یه جمله انگلیسی درباره دوستی بنویس",
    "یه جمله انگلیسی درباره آب و هوا بنویس",
    "یه جمله انگلیسی درباره سلامتی بنویس",
    "یه جمله انگلیسی درباره تحصیل و دانشگاه بنویس",
    "یه جمله انگلیسی درباره تکنولوژی بنویس",
    "یه جمله انگلیسی درباره ورزش بنویس",
]

def generate_lesson():
    """یه درس کامل با ۳ جمله انگلیسی، تلفظ و معنی تولید می‌کنه"""
    topic = random.choice(TOPICS)
    
    prompt = f"""
    {topic}
    
    دقیقاً ۳ جمله کوتاه انگلیسی (حداکثر ۱۰ کلمه) بنویس.
    برای هر جمله، این اطلاعات رو به این فرمت بده:
    
    جمله انگلیسی
    تلفظ: (تلفظ کلمه به کلمه به فارسی)
    معنی: (ترجمه فارسی)
    
    بعد از ۳ جمله، این بخش رو اضافه کن:
    
    📚 کلمات مهم:
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    - کلمه انگلیسی: معنی فارسی
    
    فقط این فرمت رو رعایت کن. توضیح اضافه نده.
    """
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "تو یه معلم زبان انگلیسی هستی که جملات کوتاه روزمره با تلفظ و معنی فارسی آموزش می‌دی."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def send_to_telegram(text):
    """متن رو به تلگرام می‌فرسته"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    r = requests.post(url, json=payload)
    return r.status_code == 200

# حلقه اصلی
print("ربات شروع شد...")

while True:
    try:
        lesson = generate_lesson()
        
        if send_to_telegram(lesson):
            print(f"✅ پست ارسال شد")
        else:
            print(f"❌ خطا در ارسال")
        
        time.sleep(900)
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        time.sleep(60)
