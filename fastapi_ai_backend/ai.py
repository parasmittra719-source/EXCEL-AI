import google.generativeai as genai
import os

# Configure using provided key or environment variable
KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBo7SnFvySEMUk3ERmfY5-bQfY-wWjF4-I")
genai.configure(api_key=KEY)

def generate_insight(data):
    try:
        # Use Gemini 2.0 Flash model
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"Analyze this business data and provide 3 concise key insights:\n{data}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"AI Error: {str(e)}"
