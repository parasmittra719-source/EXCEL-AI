from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.linear_model import LinearRegression
from auth import login
from ai import generate_insight

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
