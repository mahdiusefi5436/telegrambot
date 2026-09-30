import os
import requests
import random
import time
import re
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# آدرس صفحه‌ای که می‌خوای ازش متن برداری
SOURCE_URL = "https://taw-bio.ir/f/arc/text/all~1~all~bst"

def get_texts():
    """متن‌ها رو از سایت می‌خونه"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(SOURCE_URL, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # همه متن‌های داخل تگ‌های p یا div رو جمع می‌کنه
    texts = []
    for tag in soup.find_all(["p", "div", "span"]):
        text = tag.get_text(strip=True)
        # فقط متن‌هایی که بین ۲۰ تا ۳۰۰ کاراکتر هستن
        if 20 < len(text) < 300:
            texts.append(text)
    
    return texts

def send_to_telegram(text):
    """متن رو به تلگرام می‌فرسته"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    return r.status_code == 200

# حلقه اصلی
print("ربات شروع شد...")

while True:
    try:
        # متن‌ها رو از سایت بگیر
        all_texts = get_texts()
        
        if len(all_texts) < 4:
            print("❌ متن کافی پیدا نشد")
            time.sleep(300)
            continue
        
        # ۴ تا متن تصادفی انتخاب کن
        selected = random.sample(all_texts, 4)
        
        # با فاصله به هم بچسبون
        final_text = "\n\n➖➖➖\n\n".join(selected)
        
        # بفرست
        if send_to_telegram(final_text):
            print(f"✅ پست ارسال شد")
        else:
            print(f"❌ خطا در ارسال")
        
        # 5 دقیقه صبر کن
        time.sleep(300)
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        time.sleep(60)
