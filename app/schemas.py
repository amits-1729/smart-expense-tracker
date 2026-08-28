from pydantic import BaseModel, EmailStr
from datetime import date
from decimal import Decimal
from typing import Optional, Literal

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str



class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CategoryCreate(BaseModel):
    name: str


# class ExpenseCreate(BaseModel):
#     category_id: int
#     amount: float
#     description: str | None = None
#     expense_date: date
#     payment_method: str

# class ExpenseUpdate(BaseModel):
#     category_id: int
#     amount: float
#     description: str | None = None
#     expense_date: date
#     payment_method: str

# class ExpenseFilter(BaseModel):
#     min_amount:Optional[float] = None
#     max_amount:Optional[float] = None
#     payment_method:Optional[str] = None
#     category_id:Optional[int] = None
#     start_date:Optional[date] = None
#     end_date:Optional[date] = None

class AccountCreate(BaseModel):
    name:str

class TransactionCreate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    type: Literal["INCOME", "EXPENSE"]
    amount: Decimal
    description: Optional[str] = None
    transaction_date: date

class TransactionUpdate(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    type: Literal["INCOME", "EXPENSE"]
    amount: Decimal
    description: Optional[str] = None
    transaction_date: date

class TransactionFilter(BaseModel):
    min_amount:Optional[float] = None
    max_amount:Optional[float] = None
    account_id:Optional[int] = None # Cash/UPI/
    category_id:Optional[int] = None
    start_date:Optional[date] = None
    end_date:Optional[date] = None
    type: Literal["INCOME", "EXPENSE"] = "EXPENSE"

class BudgetCreate(BaseModel):
    category_id: int
    amount: float
    month: str


class BudgetUpdate(BaseModel):
    category_id: int
    amount: float
    month: str