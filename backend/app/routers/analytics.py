from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Income, Expense, CropProduction

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):

    incomes = db.query(Income).all()
    expenses = db.query(Expense).all()
    crops = db.query(CropProduction).all()

    total_income = sum(float(i.total_amount) for i in incomes)

    total_expenses = sum(float(e.amount) for e in expenses)

    net_profit = total_income - total_expenses

    total_acres = sum(float(c.acres_used) for c in crops)

    total_yield = sum(float(c.actual_yield_kg) for c in crops)

    revenue_per_acre = (
        total_income / total_acres
        if total_acres > 0 else 0
    )

    expense_per_acre = (
        total_expenses / total_acres
        if total_acres > 0 else 0
    )

    yield_per_acre = (
        total_yield / total_acres
        if total_acres > 0 else 0
    )

    net_profit_margin = (
        (net_profit / total_income) * 100
        if total_income > 0 else 0
    )

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_profit": round(net_profit, 2),
        "revenue_per_acre": round(revenue_per_acre, 2),
        "expense_per_acre": round(expense_per_acre, 2),
        "yield_per_acre": round(yield_per_acre, 2),
        "net_profit_margin_percent": round(net_profit_margin, 2)
    }