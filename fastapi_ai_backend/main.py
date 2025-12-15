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
        targets = data.get("targets", [])
        
        # Backward compatibility for single target
        if "target" in data and not targets:
            targets = [data["target"]]

        if not targets:
            raise HTTPException(status_code=400, detail="No target columns provided.")

        forecasts = {}
        
        df["index"] = range(len(df))
        future = [[i] for i in range(len(df), len(df)+6)]

        for target in targets:
            if target not in df.columns:
                continue # Skip invalid columns
            
            # Data validation per column
            if not pd.api.types.is_numeric_dtype(df[target]):
                continue

            # Prepare data
            sub_df = df[["index", target]].dropna()
            if len(sub_df) < 2:
                continue

            X = sub_df[["index"]]
            y = sub_df[target]

            model = LinearRegression()
            model.fit(X, y)
            preds = model.predict(future)
            forecasts[target] = preds.tolist()

        if not forecasts:
             raise HTTPException(status_code=400, detail="Could not generate forecast for any of the selected columns.")

        return {"forecasts": forecasts}
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
