from fastapi import FastAPI, WebSocket, HTTPException
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.linear_model import LinearRegression
from auth import login
from ai import generate_insight
from emailer import send_report

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.post("/forecast")
def forecast(data: dict):
    try:
        df = pd.DataFrame(data["rows"])
        target = data["target"]

        if target not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{target}' not found in dataset.")

        # Basic data validation
        if not pd.api.types.is_numeric_dtype(df[target]):
             raise HTTPException(status_code=400, detail=f"Target column '{target}' must contain numeric values.")

        df["index"] = range(len(df))
        X = df[["index"]]
        y = df[target]
        
        # Handle NaN values
        if df[target].isnull().any():
             df = df.dropna(subset=[target])
             X = df[["index"]]
             y = df[target]

        if len(df) < 2:
             raise HTTPException(status_code=400, detail="Not enough data points to forecast (need at least 2).")

        model = LinearRegression()
        model.fit(X, y)

        future = [[i] for i in range(len(df), len(df)+6)]
        preds = model.predict(future)

        return {"forecast": preds.tolist()}
    except Exception as e:
        print(f"Forecast Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
def login_api(payload: dict):
    return {"token": login(payload["username"], payload["password"])}

@app.post("/insight")
def insight(payload: dict):
    return {"insight": generate_insight(payload["data"])}

@app.post("/email-report")
async def email_report(payload: dict):
    await send_report(payload["email"], payload["content"])
    return {"status": "sent"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(10) # Push refresh every 10s
        await websocket.send_text("refresh")
