from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Inventory
from app.schemas import InventoryCreate, InventoryResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/", response_model=InventoryResponse)
def add_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    new_inventory = Inventory(
        item_name=inventory.item_name,
        category=inventory.category,
        quantity=inventory.quantity,
        unit=inventory.unit,
        unit_price=inventory.unit_price,
        reorder_level=inventory.reorder_level
    )

    db.add(new_inventory)

    db.commit()

    db.refresh(new_inventory)

    return new_inventory


@router.get("/", response_model=list[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):

    return db.query(Inventory).all()