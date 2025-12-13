from langchain_google_genai import ChatGoogleGenerativeAI
import mss
import mss.tools
from PIL import Image
import base64
from io import BytesIO

def get_llm(api_key: str = None, use_vision: bool = False):
    """Initialize Gemini LLM."""
    if not api_key:
        raise ValueError("Google API Key not provided")
    
    model = "gemini-2.0-flash" if not use_vision else "gemini-2.0-flash"
    return ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=0.3)

def take_screenshot(output_path: str = "screenshot.png") -> str:
    """Take a screenshot of the entire screen."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
    return output_path

def image_to_base64(image_path: str) -> str:
    """Convert image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
