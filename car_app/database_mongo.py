# database_mongo.py

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# 1. MongoDB Connection Setup
MONGO_DETAILS = "mongodb://localhost:27017" # Update this if your URI is different

try:
    # Initialize the client, database, and collection
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client.car_info_db # Change 'car_info_db' to your desired database name
    car_collection = database.get_collection("cars") # Change 'cars' to your desired collection name
except Exception as e:
    # Handle connection errors (e.g., if MongoDB is not running)
    print(f"Error connecting to MongoDB: {e}")
    # You might want to exit or use a placeholder here, but for development, continue.


# 2. Helper Function (Essential Fix from previous request)
def car_helper(car) -> dict:
    """Converts a MongoDB document (with ObjectId) to a dictionary (with str ID)."""
    return {
        # 👇 CRITICAL FIX: Convert the ObjectId to a string explicitly
        "id": str(car.get("_id")), 
        "car_name": car.get("car_name"),
        "company_name": car.get("company_name"),
        "price": car.get("price"),
        "mileage": car.get("mileage"),
    }