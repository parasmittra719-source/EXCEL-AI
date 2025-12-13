from langgraph.graph import StateGraph, END
from src.state import GraphState
from src.agents.vision_analyzer import vision_analyzer_node
from src.agents.workflow_planner import workflow_planner_node
from src.agents.executor import executor_node
from src.agents.validator import validator_node

def create_graph():
    """Create the LangGraph workflow for the autonomous RPA agent."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("vision_analyzer", vision_analyzer_node)
    workflow.add_node("workflow_planner", workflow_planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("validator", validator_node)
    
    # Define edges (sequential flow)
    workflow.set_entry_point("vision_analyzer")
    workflow.add_edge("vision_analyzer", "workflow_planner")
    workflow.add_edge("workflow_planner", "executor")
    workflow.add_edge("executor", "validator")
    workflow.add_edge("validator", END)
    
    return workflow.compile()
