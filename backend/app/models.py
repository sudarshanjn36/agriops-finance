from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from .database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100))
    amount = Column(Numeric(12, 2))
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100))
    quantity = Column(Numeric(12, 2))
    price_per_unit = Column(Numeric(12, 2))
    total_amount = Column(Numeric(12, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class CropProduction(Base):
    __tablename__ = "crop_production"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100))
    season = Column(String(100))
    acres_used = Column(Numeric(12, 2))
    expected_yield_kg = Column(Numeric(12, 2))
    actual_yield_kg = Column(Numeric(12, 2))
    selling_price_per_kg = Column(Numeric(12, 2))
    total_revenue = Column(Numeric(12, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    item_name = Column(String(100))

    category = Column(String(100))

    quantity = Column(Numeric(12, 2))

    unit = Column(String(50))

    unit_price = Column(Numeric(12, 2))

    reorder_level = Column(Numeric(12, 2))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BalanceSheetItem(Base):
    __tablename__ = "balance_sheet_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(150))
    item_type = Column(String(50))
    category = Column(String(100))
    amount = Column(Numeric(12, 2))
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())