from fastapi import FastAPI

from app.database import Base, engine
from app.routers import income, expenses, dashboard, crops

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgriOps Finance API")

app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(dashboard.router)
app.include_router(crops.router)

@app.get("/")
def home():
    return {"message": "AgriOps Backend Running"}