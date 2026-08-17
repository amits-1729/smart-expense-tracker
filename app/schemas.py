from pydantic import BaseModel, EmailStr
from datetime import date

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str



class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CategoryCreate(BaseModel):
    name: str


class ExpenseCreate(BaseModel):
    category_id: int
    amount: float
    description: str | None = None
    expense_date: date
    payment_method: str

class ExpenseUpdate(BaseModel):
    category_id: int
    amount: float
    description: str | None = None
    expense_date: date
    payment_method: str



class BudgetCreate(BaseModel):
    category_id: int
    amount: float
    month: str


class BudgetUpdate(BaseModel):
    category_id: int
    amount: float
    month: str