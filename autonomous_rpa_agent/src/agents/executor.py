from src.state import GraphState
import pyautogui
import time

def executor_node(state: GraphState, config: dict = None):
    """
    Executes the planned workflow using pyautogui.
    Performs clicks, typing, and other UI interactions.
    """
    workflow_plan = state["workflow_plan"]
    execution_log = []
    
    # Safety: Set a failsafe
    pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
    pyautogui.PAUSE = 1  # Pause 1 second between actions
    
    for step in workflow_plan:
        action = step["action"]
        target = step["target"]
        value = step.get("value")
        
        try:
            if action == "click":
                # For now, we'll use a simple heuristic to find elements
                # In production, this would use OCR or more sophisticated methods
                execution_log.append(f"ACTION: Click on '{target}' (Manual positioning required)")
                # Placeholder: pyautogui.click(x, y)
                
            elif action == "type":
                execution_log.append(f"ACTION: Type '{value}' into '{target}'")
                if value:
                    pyautogui.typewrite(str(value), interval=0.1)
                    
            elif action == "wait":
                wait_time = value or 2
                execution_log.append(f"ACTION: Wait {wait_time} seconds")
                time.sleep(wait_time)
                
            elif action == "scroll":
                direction = value or "down"
                execution_log.append(f"ACTION: Scroll {direction}")
                scroll_amount = 300 if direction == "down" else -300
                pyautogui.scroll(scroll_amount)
                
            elif action == "press":
                key = value or "enter"
                execution_log.append(f"ACTION: Press key '{key}'")
                pyautogui.press(key)
                
            else:
                execution_log.append(f"WARNING: Unknown action '{action}' skipped")
                
        except Exception as e:
            execution_log.append(f"ERROR: {action} on '{target}' failed: {str(e)}")
    
    return {"execution_log": execution_log}
