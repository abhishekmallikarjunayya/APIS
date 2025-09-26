from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI()

# Request body model
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

# Temporary in-memory "database"
items_db = {}

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Storage!"}

# Create an item and store it in memory
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items_db[item_id] = item
    return {"message": "Item created successfully", "item_id": item_id, "item": item}

# Read item back from memory
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id in items_db:
        return {"item_id": item_id, "item": items_db[item_id]}
    return {"error": "Item not found"}

# List all items
@app.get("/items/")
def list_items():
    return {"all_items": items_db}

# Note: This is in-memory only → if you stop the server, the data is gone.
#FastAPI app:
#GET / → just returns {"message": "Hello, FastAPI!"}
#GET /items/{item_id} → fetches an item by ID
#POST /items/ → creates a new item from JSON data you send