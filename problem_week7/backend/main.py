from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Week 07 — Items API")


# ---------- Models ----------

class ItemCreate(BaseModel):
    name: str
    price: float


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float


# Part A: every field optional -> partial update
class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


# Part D: envelope for list responses
class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


# Part E: toy prediction models (Field() = constraints for body fields)
class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float = Field(ge=0)


class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"


# ---------- In-memory storage ----------

_items: list[ItemPublic] = []
_next_id = 1


def _find(item_id: int) -> ItemPublic | None:
    for item in _items:
        if item.id == item_id:
            return item
    return None


def _get_or_404(item_id: int) -> ItemPublic:
    item = _find(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Part C: case-insensitive duplicate check; exclude_id skips the item being renamed
def _ensure_name_available(name: str, exclude_id: int | None = None) -> None:
    for item in _items:
        if item.id != exclude_id and item.name.lower() == name.lower():
            raise HTTPException(status_code=409, detail="Item with this name already exists")


# ---------- Routes ----------

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


@app.get("/items", response_model=ItemListResponse)
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_price: float | None = None,
    max_price: float | None = None,
    q: str | None = Query(None, min_length=2),
    sort_by: str = Query("id", pattern="^(id|name|price)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    # 1. Filter
    result = _items
    if min_price is not None:
        result = [it for it in result if it.price >= min_price]
    if max_price is not None:
        result = [it for it in result if it.price <= max_price]
    if q is not None:
        result = [it for it in result if q.lower() in it.name.lower()]

    # 2. Sort
    key = (lambda it: it.name.lower()) if sort_by == "name" else (lambda it: getattr(it, sort_by))
    result = sorted(result, key=key, reverse=(order == "desc"))

    # 3. Count, then paginate
    total = len(result)
    return ItemListResponse(items=result[skip:skip + limit], total=total, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    return _get_or_404(item_id)


@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global _next_id
    _ensure_name_available(data.name)
    item = ItemPublic(id=_next_id, name=data.name, price=data.price)
    _items.append(item)
    _next_id += 1
    return item


@app.put("/items/{item_id}", response_model=ItemPublic)
def replace_item(item_id: int, data: ItemCreate):
    item = _get_or_404(item_id)
    if data.name.lower() != item.name.lower():
        _ensure_name_available(data.name, exclude_id=item_id)
    item.name = data.name
    item.price = data.price
    return item


@app.patch("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, data: ItemUpdate):
    item = _get_or_404(item_id)
    # Only fields the client actually sent; explicit nulls are ignored (name/price can't be empty)
    changes = {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}
    if "name" in changes and changes["name"].lower() != item.name.lower():
        _ensure_name_available(changes["name"], exclude_id=item_id)
    for field, value in changes.items():
        setattr(item, field, value)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    item = _get_or_404(item_id)
    _items.remove(item)
    return Response(status_code=204)


@app.post("/predict/house-price", response_model=HousePricePrediction)
def predict_house_price(data: HousePriceRequest):
    # Swap this formula for model.predict(...) once a real model is trained
    price = (
        data.area_sqm * 15_000_000
        - data.distance_to_center_km * 5_000_000
        + data.bedrooms * 20_000_000
    )
    return HousePricePrediction(predicted_price=price)


app.mount("/static", StaticFiles(directory="../frontend", html=True), name="static")
