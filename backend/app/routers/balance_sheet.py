from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import BalanceSheetItem
from app.schemas import BalanceSheetCreate, BalanceSheetResponse

router = APIRouter(prefix="/balance-sheet", tags=["Balance Sheet"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BalanceSheetResponse)
def add_balance_sheet_item(
    item: BalanceSheetCreate,
    db: Session = Depends(get_db)
):
    new_item = BalanceSheetItem(
        item_name=item.item_name,
        item_type=item.item_type,
        category=item.category,
        amount=item.amount,
        description=item.description
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/", response_model=list[BalanceSheetResponse])
def get_balance_sheet_items(db: Session = Depends(get_db)):
    return db.query(BalanceSheetItem).all()


@router.get("/summary")
def get_balance_sheet_summary(db: Session = Depends(get_db)):
    items = db.query(BalanceSheetItem).all()

    total_assets = sum(
        float(i.amount) for i in items
        if i.item_type.lower() == "asset"
    )

    total_liabilities = sum(
        float(i.amount) for i in items
        if i.item_type.lower() == "liability"
    )

    total_equity = sum(
        float(i.amount) for i in items
        if i.item_type.lower() == "equity"
    )

    calculated_equity = total_assets - total_liabilities
    balance_difference = calculated_equity - total_equity

    return {
        "total_assets": round(total_assets, 2),
        "total_liabilities": round(total_liabilities, 2),
        "total_equity_entered": round(total_equity, 2),
        "calculated_equity": round(calculated_equity, 2),
        "balance_difference": round(balance_difference, 2),
        "is_balanced": abs(balance_difference) < 0.01
    }