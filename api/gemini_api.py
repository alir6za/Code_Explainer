import requests

GEMINI_API_KEY = "YOUR_API_KEY"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_code_explanation(code_text):
    prompt = f"""این کد را به صورت مختصر و مفید تشریح کن:
- هدف اصلی کد چیست؟
- اگر نکته مهمی وجود دارد، ذکر کن
کد:
{code_text}
پاسخ را به فارسی و در حداکثر ۳-۴ خط ارائه بده."""
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        explanation = result['candidates'][0]['content']['parts'][0]['text']
        return explanation.strip()
    except Exception as e:
        return f"Error getting description: {str(e)}"
