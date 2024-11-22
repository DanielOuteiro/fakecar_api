from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import random
import string
import uuid
from datetime import datetime
import uvicorn

app = FastAPI()

# Data Models
class CarData(BaseModel):
    brand: str
    model: str
    year: int
    vin: str
    license_plate: str
    infotainment_capabilities: List[str]
    color: str
    charging_port_location: str
    battery_capacity: float
    maximum_range: float
    charging_connector_types: List[str]
    charging_cable_types: List[str]
    gps_coordinates: Dict[str, float]
    state_of_charge: float
    speed: float
    instant_power_consumption: float
    historical_power_consumption: List[float]
    range_estimation: float
    charging_status: str
    charging_power_rate: float
    battery_temperature: float
    error_codes: List[str]
    motor_rpm: float
    odometer_reading: float
    battery_12v_voltage: float
    regenerative_braking_data: Dict[str, float]
    tire_pressure: Dict[str, float]

class UserData(BaseModel):
    code: str
    name: str
    age: int
    language: str
    nationality: str
    phone_number: str
    car: CarData

# In-memory database
users_db: Dict[str, UserData] = {}

def generate_user_code() -> str:
    """Generate a fixed user code 'aaaaaa' for each user"""
    return "aaaaaa"

def generate_random_car() -> CarData:
    """Generate random car data with GPS coordinates fixed to Porto"""
    car_options = {
        "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
        "BMW": ["i4", "iX", "330e", "530e"],
        "Audi": ["e-tron", "Q4 e-tron", "RS e-tron GT"],
        "Mercedes": ["EQS", "EQE", "EQA", "EQB"],
        "Porsche": ["Taycan", "Taycan Cross Turismo"],
        "Volvo": ["C40", "XC40 Recharge"]
    }
    
    brand = random.choice(list(car_options.keys()))
    model = random.choice(car_options[brand])
    colors = ["Black", "White", "Blue", "Red", "Silver", "Green"]
    
    return CarData(
        brand=brand,
        model=model,
        year=random.randint(2020, 2024),
        vin=str(uuid.uuid4().hex)[:17].upper(),
        license_plate=f"{random.choice(string.ascii_uppercase)}{random.randint(100, 999)}",
        infotainment_capabilities=["Navigation", "Bluetooth", "WiFi", "Mobile App"],
        color=random.choice(colors),
        charging_port_location=random.choice(["Front", "Rear Left", "Rear Right"]),
        battery_capacity=random.uniform(60, 100),
        maximum_range=random.uniform(250, 450),
        charging_connector_types=["Type 2", "CCS"],
        charging_cable_types=["Mode 3", "Mode 4"],
        gps_coordinates={"latitude": 41.1498379795316, "longitude": -8.65870106339955},
        state_of_charge=random.uniform(0, 100),
        speed=random.uniform(0, 120),
        instant_power_consumption=random.uniform(10, 30),
        historical_power_consumption=[random.uniform(10, 30) for _ in range(10)],
        range_estimation=random.uniform(150, 350),
        charging_status=random.choice(["Charging", "Not Charging", "Scheduled"]),
        charging_power_rate=random.uniform(0, 150),
        battery_temperature=random.uniform(20, 40),
        error_codes=[],
        motor_rpm=random.uniform(0, 7000),
        odometer_reading=random.uniform(0, 50000),
        battery_12v_voltage=random.uniform(11.5, 12.8),
        regenerative_braking_data={"power": random.uniform(0, 50), "efficiency": random.uniform(0.8, 0.95)},
        tire_pressure={
            "front_left": random.uniform(2.2, 2.4),
            "front_right": random.uniform(2.2, 2.4),
            "rear_left": random.uniform(2.2, 2.4),
            "rear_right": random.uniform(2.2, 2.4)
        }
    )

def prepopulate_user():
    """Add an initial user to the database"""
    user_data = UserData(
        code=generate_user_code(),
        name="John Doe",
        age=30,
        language="English",
        nationality="US",
        phone_number="+11234567890",
        car=generate_random_car()
    )
    users_db[user_data.code] = user_data

@app.on_event("startup")
def startup_event():
    """Prepopulate user when the server starts"""
    prepopulate_user()

@app.post("/users/create")
async def create_user() -> UserData:
    """Create a new user with fixed code 'aaaaaa' and Porto coordinates"""
    names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Wilson"]
    languages = ["English", "Spanish", "French", "German"]
    nationalities = ["US", "UK", "FR", "DE", "ES"]
    
    user_data = UserData(
        code=generate_user_code(),
        name=random.choice(names),
        age=random.randint(18, 80),
        language=random.choice(languages),
        nationality=random.choice(nationalities),
        phone_number=f"+{random.randint(1, 99)}{random.randint(100000000, 999999999)}",
        car=generate_random_car()
    )
    
    users_db[user_data.code] = user_data
    return user_data

@app.get("/users/{code}")
async def get_user(code: str) -> UserData:
    """Get user data by code"""
    if code not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[code]

@app.get("/users")
async def list_users() -> List[UserData]:
    """List all users"""
    return list(users_db.values())

@app.put("/users/{code}/car/update")
async def update_car_data(code: str, car_data: CarData) -> UserData:
    """Update car data for a specific user"""
    if code not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[code].car = car_data
    return users_db[code]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
