from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, ItemDB

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
    
# Pydantic model
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

    class Config:
        orm_mode = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create an item inside a bucket
@app.post("/buckets/{bucket_name}/items/", response_model=Item)
def create_item(bucket_name: str, item: Item, db: Session = Depends(get_db)):
    db_item = ItemDB(bucket_name=bucket_name, name=item.name, price=item.price, in_stock=item.in_stock)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Read all items in a bucket
@app.get("/buckets/{bucket_name}/items/", response_model=List[Item])
def list_bucket_items(bucket_name: str, db: Session = Depends(get_db)):
    return db.query(ItemDB).filter(ItemDB.bucket_name == bucket_name).all()

# Read a single item by ID in a bucket
@app.get("/buckets/{bucket_name}/items/{item_id}", response_model=Item)
def read_item(bucket_name: str, item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.bucket_name == bucket_name, ItemDB.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# List all buckets with items
@app.get("/buckets/")
def list_all_buckets(db: Session = Depends(get_db)):
    buckets = db.query(ItemDB.bucket_name).distinct().all()
    return {"buckets": [b[0] for b in buckets]}


