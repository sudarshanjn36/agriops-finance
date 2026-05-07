from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ExpenseResponse)
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(
        category=expense.category,
        amount=expense.amount,
        description=expense.description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()