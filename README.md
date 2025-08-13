<div style="direction: rtl; text-align: right;">

## Code Explainer — ابزار توضیح خودکار کد با استفاده از کلید میانبر در لینوکس

خیلی وقت‌ها پیش میاد که می‌خوای کد رو بررسی کنی و بفهمی دقیقاً چی کار می‌کنه، اما حوصله‌ی کپی‌پیست کردنش توی ابزار هوش مصنوعی رو نداری. با این ریپو، فقط با هایلایت کردن کد و زدن یک کلید ترکیبی می‌تونی همون‌جا پنل توضیحات کد رو جلوی چشمت بیاری.

<div style="text-align: center;">
  <img src="./assets/img/sample.png" alt="panel" width="700"/>
</div>

این ابزار سبک برای لینوکس، متن کدی که انتخاب کرده‌اید را خوانده و با استفاده از LLM (مدل Gemini)، آن را به‌صورت خلاصه و به زبان فارسی توضیح می‌دهد. رابط کاربری آن با GTK3 طراحی شده و برای بستن پنجره کافی است کلید Space را فشار دهید.

## قابلیت‌ها
- **توضیح فارسی و خلاصه**: جمع‌بندی ۳–۴ خطی از هدف و نکات مهم کد  
- **پنل دو-بخشی**: نمایش همزمان «کد انتخاب‌شده» و «توضیح»  
- **هایلایت سینتکس خودکار**
- **میانبر بستن**: کلید Space  

## پیش‌نیازها
- **سیستم‌عامل**: لینوکس   
- **Python**: نسخه 3.10 یا بالاتر  
- **وابستگی‌های سیستمی**:
<div style="text-align: left; direction: ltr;">

  - Debian/Ubuntu:  
    ```bash
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip python3-gi gir1.2-gtk-3.0 xclip libnotify-bin
    ```  
  - Fedora/RHEL:  
    ```bash
    sudo dnf install -y python3 python3-pip python3-gi gtk3 xclip libnotify
    ```  
  - Arch:  
    ```bash
    sudo pacman -S --needed python python-pip python-gobject gtk3 xclip libnotify
    ```
</div>

## نصب وابستگی‌های پایتونی
در ریشه مخزن:  
```bash
cd Code_Explainer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## نحوه گرفتن API از [Studio AI](https://aistudio.google.com/prompts/new_chat)


برای استفاده از این پروژه نیاز دارید کلید API از Studio AI بگیرید.  
مراحل  دریافت API:

<a href="https://youtu.be/MziqV5U4U1o?si=iSIGzSf0d6gxK9Wd">
  <img src="./assets/img/youtube.png" alt="آموزش گرفتن API از Studio AI" width="150" />
</a>

 کلید را در فایل `api/gemini_api.py` در متغیر `GEMINI_API_KEY` جایگزین کنید.


## ساخت شورتکات اجرای ماژول در لینوکس

برای اجرای سریع ماژول `main.py` با یک کلید میانبر در لینوکس مراحل زیر را دنبال کنید:

1. ابتدا اطمینان حاصل کنید که اسکریپت قابلیت اجرا دارد:  
    ```bash
    chmod +x path/to/main.py
    ```

2. برای ساخت شورتکات اجرای ماژول در محیط دسکتاپ (مثلاً GNOME) به مسیر زیر بروید:  

    ```
    Settings → Keyboard → View and Customize Shortcuts → Customize Shortcuts
    ```

3.سپس یک شورتکات جدید بسازید و مقادیر زیر را وارد کنید: 
- **Name:** نام دلخواه (مثلاً `Code Explainer`)  
- **Command:** مسیر اجرای ماژول `main.py`، برای مثال:  
  ```bash
  python3 /full/path/to/main.py
  ```
- **Shortcut:** کلید ترکیبی دلخواه (مثلاً Ctrl+Q)

4. شورتکات ذخیره‌شده را تست کنید؛ با فشردن کلید تعریف‌شده، اسکریپت اجرا خواهد شد.
</div>

