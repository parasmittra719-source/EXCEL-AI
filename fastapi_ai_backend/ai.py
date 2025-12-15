import google.generativeai as genai
import os

# Configure using provided key or environment variable
KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBo7SnFvySEMUk3ERmfY5-bQfY-wWjF4-I")
genai.configure(api_key=KEY)

import time

def generate_insight(data):
    # Retry logic (3 attempts with exponential backoff)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Use Stable Flash model (usually 1.5-flash)
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = f"Analyze this business data and provide 3 concise key insights:\n{data}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2 # 2s, 4s, 6s...
                    print(f"Gemini 429 Quota Error. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                     return "AI Busy: Quota exceeded. Please try again later."
            print(f"Gemini Error: {e}")
            return f"AI Error: {str(e)}"
