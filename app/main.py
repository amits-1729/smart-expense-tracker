from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.dependencies import get_current_user
from app.routes.categories import router as category_router
from app.routes.expenses import router as expense_router
from app.routes.budgets import router as budget_router

app = FastAPI(title="Smart Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(budget_router)


@app.get("/")
def root():
    return {"message": "Smart Expense Tracker API is running"}

@app.get("/test-auth")
def test_auth(user_id: int = Depends(get_current_user)):
    return {
        "message": "Authentication successful",
        "user_id": user_id
    }