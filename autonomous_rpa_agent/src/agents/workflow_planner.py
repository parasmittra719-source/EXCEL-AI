from langchain_core.prompts import ChatPromptTemplate
from src.utils import get_llm
from src.state import GraphState
import json

def workflow_planner_node(state: GraphState, config: dict = None):
    """
    Plans the automation workflow based on UI analysis.
    Creates a step-by-step action plan.
    """
    config = config or {}
    api_key = config.get("configurable", {}).get("api_key") or state.get("api_key")
    llm = get_llm(api_key)
    
    task = state["task_description"]
    ui_analysis = state["ui_analysis"]
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are an automation planner. Based on the UI analysis, create a detailed workflow plan.
        
        Task: {task}
        
        UI Analysis:
        {ui_analysis}
        
        Create a JSON array of steps to automate this task. Each step should have:
        - "action": The type of action (click, type, wait, scroll, etc.)
        - "target": Description of the element to interact with
        - "value": The value to input (for typing actions), or null
        - "reasoning": Why this step is necessary
        
        Example:
        [
            {{"action": "click", "target": "Email field at top-left", "value": null, "reasoning": "Focus on email input"}},
            {{"action": "type", "target": "Email field", "value": "test@example.com", "reasoning": "Enter email address"}},
            {{"action": "click", "target": "Submit button at bottom-right", "value": null, "reasoning": "Submit the form"}}
        ]
        
        Return ONLY the JSON array, no additional text.
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({"task": task, "ui_analysis": ui_analysis})
    
    # Parse JSON workflow
    try:
        workflow_plan = json.loads(response.content.strip())
    except:
        # Fallback if JSON parsing fails
        workflow_plan = [{
            "action": "error",
            "target": "N/A",
            "value": None,
            "reasoning": "Failed to generate valid workflow plan"
        }]
    
    return {"workflow_plan": workflow_plan}
