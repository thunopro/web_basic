from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/house_form.html")

def predict_price(area: float, bedrooms: int, location: str = "other") -> float:
    price = 500000000.0 + area * 15000000.0 + bedrooms * 50000000.0
    loc = location.lower()
    if loc == "hanoi":
        price *= 1.3
    elif loc == "hcmc":
        price *= 1.25
    return round(price, -6)

@app.get("/predict")
def predict(area: float, bedrooms: int, location: str = "other"):
    predicted_price = predict_price(area, bedrooms, location)
    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "predicted_price": predicted_price
    }

class HouseInput(BaseModel):
    area: float
    bedrooms: int
    location: str = "other"

@app.post("/predict")
def predict_post(house: HouseInput):
    predicted_price = predict_price(house.area, house.bedrooms, house.location)
    return {
        "area": house.area,
        "bedrooms": house.bedrooms,
        "location": house.location,
        "predicted_price": predicted_price
    }

app.mount("/static", StaticFiles(directory="../frontend"), name="static")
