from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Finance Coach API"}

@app.get("/summary")
def summary():
    df = pd.read_csv("cleaned_data.csv")
    income = df[df['Amount'] > 0]['Amount'].sum()
    expense = df[df['Amount'] < 0]['Amount'].sum()
    return {"income": income, "expense": expense}