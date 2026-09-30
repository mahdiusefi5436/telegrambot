import os
import requests
import random
import time
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# موضوعاتی که از سایت برداشته می‌شن
CATEGORIES = [
    "shaytan",     # شیطنت
    "refaghati",   # رفاقتی
    "asabani",     # عصیانی
    "eqtesadi",    # اقتصادی
    "tike-dar",    # تیکه دار
    "qamgin",      # غمگین
    "tanhayi",     # تنهایی
    "asheqane",    # عاشقانه
]

def get_texts_from_site(category):
    """متن‌ها رو از یه دسته‌ی سایت می‌خونه"""
    url = f"https://taw-bio.ir/f/arc/text/all~1~all~{category}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        texts = []
        for tag in soup.find_all(["p", "div", "span", "h3"]):
            text = tag.get_text(strip=True)
            if 20 < len(text) < 300:
                texts.append(text)
        
        return texts
    except Exception as e:
        print(f"❌ خطا در خواندن {category}: {e}")
        return []

def send_to_telegram(text):
    """متن رو به تلگرام می‌فرسته (با فرمت نقل قول)"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # هر متن رو توی نقل قول می‌ذاریم
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
        all_texts = []
        
        # از ۳ تا دسته‌ی تصادفی، متن جمع کن
        selected_categories = random.sample(CATEGORIES, 3)
        
        for cat in selected_categories:
            texts = get_texts_from_site(cat)
            if texts:
                all_texts.extend(texts)
        
        if len(all_texts) < 10:
            print("❌ متن کافی پیدا نشد، دوباره تلاش می‌کنم...")
            time.sleep(60)
            continue
        
        # ۱۰ تا متن تصادفی انتخاب کن
        selected = random.sample(all_texts, 10)
        
        # هر متن رو توی نقل قول بذار و با فاصله به هم بچسبون
        formatted = []
        for t in selected:
            formatted.append(f"<blockquote>{t}</blockquote>")
        
        final_text = "\n\n➖➖➖\n\n".join(formatted)
        
        # اگه طولانی بود، کوتاهش کن (تلگرام حداکثر ۴۰۹۶ کاراکتر قبول می‌کنه)
        if len(final_text) > 4000:
            final_text = final_text[:4000] + "..."
        
        if send_to_telegram(final_text):
            print(f"✅ پست ارسال شد با {len(selected)} متن")
        else:
            print(f"❌ خطا در ارسال")
        
        time.sleep(300)
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        time.sleep(60)
