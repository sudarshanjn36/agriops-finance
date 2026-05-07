from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database import SessionLocal
from app.models import Income
from app.schemas import IncomeCreate, IncomeResponse

router = APIRouter(prefix="/income", tags=["Income"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=IncomeResponse)
def add_income(income: IncomeCreate, db: Session = Depends(get_db)):
    total_amount = income.quantity * income.price_per_unit

    new_income = Income(
        crop_name=income.crop_name,
        quantity=income.quantity,
        price_per_unit=income.price_per_unit,
        total_amount=total_amount
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income

@router.get("/", response_model=list[IncomeResponse])
def get_income(db: Session = Depends(get_db)):
    return db.query(Income).all()