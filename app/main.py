from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(title="Smart Expense Tracker API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Smart Expense Tracker API is running"}