from fastapi import FastAPI, WebSocket
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.post("/forecast")
def forecast(data: dict):
    df = pd.DataFrame(data["rows"])
    target = data["target"]

    df["index"] = range(len(df))
    X = df[["index"]]
    y = df[target]

    model = LinearRegression()
    model.fit(X, y)

    future = [[i] for i in range(len(df), len(df)+6)]
    preds = model.predict(future)

    return {"forecast": preds.tolist()}

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
