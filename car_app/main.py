# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
from models import Car
from database_mongo import car_collection, car_helper # car_helper is still needed for get_cars
from bson import ObjectId
import os

app = FastAPI(title="Car Info App")

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def read_index():
    path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(path, "r") as f:
        return f.read()

# GET all cars - uses car_helper
@app.get("/cars/", response_model=List[Car])
async def get_cars():
    cars = []
    async for car in car_collection.find():
        # car_helper is needed here to convert all items before they are added to the list
        cars.append(car_helper(car)) 
    return cars

# GET a car by ID - relies on response_model
@app.get("/cars/{id}", response_model=Car)
async def get_car(id: str):
    # This works because response_model=Car and Car.Config allows population by field name
    car = await car_collection.find_one({"_id": ObjectId(id)})
    if car:
        return car # FastAPI/Pydantic automatically handles the _id to id conversion
    raise HTTPException(status_code=404, detail="Car not found")

# POST a new car - relies on response_model
@app.post("/cars/", response_model=Car)
async def create_car(car: Car):
    # Fix: We must manually remove the potential 'id' from the incoming model before insert
    car_dict = car.dict(by_alias=True, exclude_none=True, exclude={"id"})
    
    new_car = await car_collection.insert_one(car_dict)
    created_car = await car_collection.find_one({"_id": new_car.inserted_id})
    return created_car # FastAPI/Pydantic automatically handles the _id to id conversion

# PUT (update) a car by ID - relies on response_model
@app.put("/cars/{id}", response_model=Car)
async def update_car(id: str, car: Car):
    # Fix: Ensure we use the Pydantic model to dict conversion for proper MongoDB storage
    # Also exclude 'id' to prevent trying to update the immutable _id field
    car_dict = car.dict(by_alias=True, exclude_none=True, exclude={"id"})

    result = await car_collection.update_one({"_id": ObjectId(id)}, {"$set": car_dict})
    if result.modified_count == 1:
        updated_car = await car_collection.find_one({"_id": ObjectId(id)})
        return updated_car # FastAPI/Pydantic automatically handles the _id to id conversion
    
    # If modified_count is 0, it might mean the car wasn't found or data was identical.
    # We'll check if it exists before throwing 404
    if not await car_collection.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404, detail="Car not found")
    
    # If it was found but not modified (data was the same), return the existing one.
    return await car_collection.find_one({"_id": ObjectId(id)})


# DELETE a car by ID
@app.delete("/cars/{id}")
async def delete_car(id: str):
    result = await car_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"status": "Car deleted"}
    raise HTTPException(status_code=404, detail="Car not found")