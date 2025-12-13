import gradio as gr
from src.graph import create_graph
import json

def run_automation(task_description, api_key):
    """
    Run the autonomous RPA agent.
    """
    if not task_description or not api_key:
        return "❌ Please provide both a task description and API key."
    
    try:
        # Create the workflow graph
        graph = create_graph()
        
        # Initialize state
        initial_state = {
            "task_description": task_description,
            "screenshot_path": None,
            "ui_analysis": None,
            "workflow_plan": None,
            "execution_log": None,
            "validation_result": None,
            "api_key": api_key
        }
        
        # Configure with API key
        config = {
            "configurable": {
                "api_key": api_key
            }
        }
        
        # Run the workflow
        result = graph.invoke(initial_state, config)
        
        # Format output
        output = f"""
## 🔍 UI Analysis
{result.get('ui_analysis', 'N/A')}

---

## 📋 Workflow Plan
```json
{json.dumps(result.get('workflow_plan', []), indent=2)}
```

---

## 🤖 Execution Log
{chr(10).join(result.get('execution_log', ['No actions executed']))}

---

## ✅ Validation Result
{result.get('validation_result', 'N/A')}
        """
        
        return output
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Create Gradio UI
with gr.Blocks(title="Autonomous RPA Agent") as demo:
    gr.Markdown("# 🤖 Autonomous RPA Agent")
    gr.Markdown("Automate any software by analyzing UI and executing workflows autonomously.")
    
    with gr.Row():
        with gr.Column():
            task_input = gr.Textbox(
                label="Task Description",
                placeholder="Example: Fill out the contact form with name 'John Doe' and email 'john@example.com'",
                lines=3
            )
            api_key_input = gr.Textbox(
                label="Gemini API Key",
                type="password",
                placeholder="Enter your Google API Key"
            )
            run_btn = gr.Button("🚀 Automate", variant="primary")
        
        with gr.Column():
            output = gr.Markdown(label="Results")
    
    run_btn.click(
        fn=run_automation,
        inputs=[task_input, api_key_input],
        outputs=output
    )
    
    gr.Markdown("""
    ### ⚠️ Important Notes:
    - **Safety**: Move your mouse to the top-left corner to abort automation
    - **Testing**: Start with simple tasks to test the agent
    - **Permissions**: Ensure the app has screen recording permissions
    - **Works Best**: On web forms, simple desktop apps with clear UI elements
    """)

if __name__ == "__main__":
    demo.launch()
