from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from src.utils import get_llm, take_screenshot, image_to_base64
from src.state import GraphState
import os

def vision_analyzer_node(state: GraphState, config: dict = None):
    """
    Analyzes the current screen using Gemini Vision.
    Identifies UI elements, fields, buttons, and their relationships.
    """
    config = config or {}
    api_key = config.get("configurable", {}).get("api_key") or state.get("api_key")
    
    # Take screenshot
    screenshot_path = take_screenshot("current_screen.png")
    
    # Use Gemini Vision to analyze UI
    llm = get_llm(api_key, use_vision=True)
    
    prompt = f"""
    Analyze this screenshot of a software interface. 
    Task: {state['task_description']}
    
    Provide:
    1. **UI Elements**: List all visible buttons, input fields, dropdowns, links with their approximate positions (top-left, center, etc.)
    2. **Layout**: Describe the overall layout (form, table, navigation bar, etc.)
    3. **Relevant Elements**: Which elements are most relevant to completing the task?
    4. **Suggested First Action**: What should be the first action to complete the task?
    
    Be specific and actionable.
    """
    
    # Read image and convert to base64
    image_b64 = image_to_base64(screenshot_path)
    
    # Create message with image
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image_b64}"
            }
        ]
    )
    
    response = llm.invoke([message])
    ui_analysis = response.content
    
    return {
        "screenshot_path": screenshot_path,
        "ui_analysis": ui_analysis
    }
