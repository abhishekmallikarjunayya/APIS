from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from storage import load_items, save_items  # Import JSON storage helpers

app = FastAPI()

# Pydantic model for request body
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

# Load items from JSON at startup
items_db: Dict[int, Dict] = load_items()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with JSON Storage!"}

# Create or update an item
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items_db[item_id] = item.dict()
    save_items(items_db)  # Persist immediately to JSON
    return {"message": "Item created successfully", "item_id": item_id, "item": item}

# Read an item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": items_db[item_id]}

# List all items
@app.get("/items/")
def list_items():
    return {"all_items": items_db}


# --------------------------------------------------------------------------- #
## How it works ##

#On server startup, it loads existing items from data.json if it exists.
#POST /items/{item_id} → Creates/updates an item and immediately saves it to data.json.
#GET /items/{item_id} → Fetch a single item by its ID.
#GET /items/ → List all items.
#data.json will be automatically created the first time you add an item.
#Items persist even after restarting the FastAPI server.