# Autonomous RPA Agent 🤖

An AI-powered agent that can automate any software by analyzing UI elements and executing workflows autonomously.

## 🚀 Features

- **Vision Analysis**: Uses Gemini Vision to analyze screenshots and identify UI elements
- **Workflow Planning**: Automatically plans step-by-step automation workflows
- **Execution**: Performs clicks, typing, and navigation using pyautogui
- **Validation**: Verifies task completion using AI vision

## 🛠️ Tech Stack

- **Python 3.9+**
- **LangGraph** (Multi-agent orchestration)
- **Gemini 2.0 Flash** (Vision + LLM)
- **pyautogui** (UI automation)
- **Gradio** (Web interface)

## 📦 Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API Key:
   ```bash
   export GOOGLE_API_KEY=your_key_here
   ```

## ▶️ Usage

Run the Gradio app:
```bash
python app.py
```

Navigate to the local URL (e.g., `http://127.0.0.1:7860`).

### Example Tasks:
- "Fill out the contact form with name 'John Doe' and email 'john@example.com'"
- "Click the login button and enter username 'testuser'"
- "Scroll down and click the submit button"

## ⚠️ Safety

- **Failsafe**: Move mouse to top-left corner of screen to abort
- **Test Carefully**: Start with simple, non-destructive tasks
- **Permissions**: Grant screen recording permissions if prompted

## 📝 How It Works

1. **Vision Analyzer**: Takes screenshot, analyzes UI elements
2. **Workflow Planner**: Creates step-by-step automation plan
3. **Executor**: Performs the planned actions
4. **Validator**: Checks if task completed successfully

## 🎯 Limitations

- Currently uses heuristic positioning (future: OCR/coordinate detection)
- Works best on web forms and simple desktop UIs
- Requires clear, specific task descriptions

## 🧪 Testing

Try the agent on:
- Google Forms
- Simple web login pages
- Desktop applications (Notepad, Calculator)
