from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Income, Expense

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):
    total_income = sum(float(i.total_amount) for i in db.query(Income).all())
    total_expenses = sum(float(e.amount) for e in db.query(Expense).all())

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_profit": total_income - total_expenses
    }