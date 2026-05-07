from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class IncomeCreate(BaseModel):
    crop_name: str
    quantity: Decimal
    price_per_unit: Decimal

class IncomeResponse(IncomeCreate):
    id: int
    total_amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    category: str
    amount: Decimal
    description: str

class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
class CropCreate(BaseModel):
    crop_name: str
    season: str
    acres_used: Decimal
    expected_yield_kg: Decimal
    actual_yield_kg: Decimal
    selling_price_per_kg: Decimal

class CropResponse(CropCreate):
    id: int
    total_revenue: Decimal
    created_at: datetime

    class Config:
        from_attributes = True