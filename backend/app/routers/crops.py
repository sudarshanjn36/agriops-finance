from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import CropProduction
from app.schemas import CropCreate, CropResponse

router = APIRouter(prefix="/crops", tags=["Crops"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CropResponse)
def add_crop(crop: CropCreate, db: Session = Depends(get_db)):
    total_revenue = crop.actual_yield_kg * crop.selling_price_per_kg

    new_crop = CropProduction(
        crop_name=crop.crop_name,
        season=crop.season,
        acres_used=crop.acres_used,
        expected_yield_kg=crop.expected_yield_kg,
        actual_yield_kg=crop.actual_yield_kg,
        selling_price_per_kg=crop.selling_price_per_kg,
        total_revenue=total_revenue
    )

    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)

    return new_crop

@router.get("/", response_model=list[CropResponse])
def get_crops(db: Session = Depends(get_db)):
    return db.query(CropProduction).all()