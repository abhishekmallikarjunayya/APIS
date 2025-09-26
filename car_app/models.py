# models.py
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId # Import ObjectId

class Car(BaseModel):
    car_name: str
    company_name: str
    price: float
    mileage: float
    # Alias the MongoDB field '_id' to the Pydantic field 'id'
    id: Optional[str] = Field(None, alias="_id")  

    class Config:
        # Keep existing config
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # 👇 CRITICAL FIX: Add json_encoders to automatically convert ObjectId to str
        json_encoders = {ObjectId: str}