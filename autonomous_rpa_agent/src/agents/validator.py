from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from src.utils import get_llm, take_screenshot, image_to_base64
from src.state import GraphState

def validator_node(state: GraphState, config: dict = None):
    """
    Validates if the automation was successful by analyzing the result.
    """
    config = config or {}
    api_key = config.get("configurable", {}).get("api_key") or state.get("api_key")
    
    # Take a new screenshot to validate result
    result_screenshot = take_screenshot("result_screen.png")
    
    llm = get_llm(api_key, use_vision=True)
    
    task = state["task_description"]
    execution_log = state["execution_log"]
    
    prompt = f"""
    Analyze this screenshot to determine if the automation task was completed successfully.
    
    Original Task: {task}
    
    Execution Log:
    {chr(10).join(execution_log)}
    
    Based on the current screen, answer:
    1. **Success**: Was the task completed? (Yes/No/Partial)
    2. **Evidence**: What visual evidence supports your conclusion?
    3. **Issues**: Any problems or errors visible?
    4. **Suggestions**: How could the automation be improved?
    
    Be specific and concise.
    """
    
    image_b64 = image_to_base64(result_screenshot)
    
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
    validation_result = response.content
    
    return {"validation_result": validation_result}
