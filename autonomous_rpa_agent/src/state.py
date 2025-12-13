from typing import TypedDict, List, Dict, Optional

class GraphState(TypedDict):
    """State for the autonomous RPA agent workflow."""
    task_description: str  # User's task description
    screenshot_path: Optional[str]  # Path to current screenshot
    ui_analysis: Optional[str]  # Vision analysis of UI elements
    workflow_plan: Optional[List[Dict]]  # Planned automation steps
    execution_log: Optional[List[str]]  # Log of executed actions
    validation_result: Optional[str]  # Success/failure validation
    api_key: Optional[str]  # Gemini API key
