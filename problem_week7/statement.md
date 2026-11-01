Week 07 — Extended Lab

    Dashboard
    My courses
    EP16.CNTT1164(126)_01
    Section 07 - FastAPI: Routing & Request/Response
    Week 07 — Extended Lab

Completion requirements
Opened: Thursday, 17 September 2026, 3:00 PM
Due: Sunday, 20 September 2026, 10:00 PM
Week 07 — Extended Lab (Lab 4, Take-Home)

FastAPI — Routing & Request/Response

This lab builds directly on top of Lab 1–2–3's main.py — do not start a new file. It is meant for students who finish the in-class labs early, or as take-home practice before Week 8 (Middleware, Dependencies & Sessions).
Part A — Partial Updates with PATCH

So far the API only supports PUT (full replace). In practice, clients often want to change one field without resending the whole object.

Requirements:

    Add PATCH /items/{item_id} using a new model ItemUpdate where every field is optional.
    Only update the fields the client actually sent; leave the rest unchanged.
    Return 404 if the item doesn't exist, exactly like the other routes.
    Response should use response_model=ItemPublic.

Hint: Pydantic v2's model_dump(exclude_unset=True) gives you a dict containing only the fields the client explicitly provided — this is the key to "only touch what was sent."

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None

Think about it: why is PATCH /items/{id} with ItemUpdate semantically different from PUT /items/{id} with ItemCreate, even if a client sends the exact same JSON body to both? (Answer to discuss in class: PUT means "this is now the complete state of the resource" — any field the client omits should logically reset to a default; PATCH means "only touch what I sent.")
Part B — Filtering, Searching & Sorting

Right now GET /items only supports skip/limit. Real APIs almost always need filtering too.

Requirements:

    Add optional query parameters: min_price: float | None, max_price: float | None.
    Add an optional q: str | None = Query(None, min_length=2) that does a case-insensitive substring match on name.
    Add sort_by: str = Query("id", pattern="^(id|name|price)$") and order: str = Query("asc", pattern="^(asc|desc)$").
    Apply filtering and sorting before slicing with skip/limit — order of operations matters here.

Common mistake: applying skip/limit slicing before filtering. If you slice first and filter second, pagination becomes meaningless (you might filter an empty page down to zero results even though matching items exist further in the list).

Exam-relevant point: Query(..., pattern="...") is exactly the same validation mechanism you already know from ge/le/min_length — regex constraints just extend the pattern to arbitrary string shapes, and they show up in /docs automatically like everything else declared with Query().
Part C — Duplicate Names & 409 Conflict

Requirements:

    Before creating an item in POST /items, check whether an item with the same name (case-insensitive) already exists.
    If it does, raise HTTPException(status_code=409, detail="Item with this name already exists") instead of creating a duplicate.
    Apply the same check in PATCH/PUT when the client is renaming an item (skip the check if the name isn't changing).

This is the first time in the course you'll use 409 for something other than a textbook example — treat it as a real design decision, not just "another status code to memorize."
Part D — Reshape the List Response (Envelope Pattern)

Currently GET /items returns a bare JSON array. Production APIs often wrap list responses in an "envelope" that carries pagination metadata alongside the data.

Requirements:

    Define:

class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int

    Change list_items's response_model to ItemListResponse, and return total as the count of items after filtering but before slicing (Part B).

This is exactly the shape most real-world paginated APIs use (GitHub's API, Stripe's API, etc.) — clients need total to render "Page 3 of 12" without fetching everything.
Part E — Bonus / DS-AI Track: A Toy Prediction Endpoint

This part is entirely optional and is meant to preview where FastAPI fits into your own DS/AI projects. It does not require an actual trained model.

Requirements:

    Add a new model HousePriceRequest with fields such as area_sqm: float, bedrooms: int, distance_to_center_km: float.
    Add POST /predict/house-price that takes a HousePriceRequest body and returns a fake prediction using a simple formula (e.g. price = area_sqm * 15_000_000 - distance_to_center_km * 5_000_000 + bedrooms * 20_000_000), wrapped in a response model HousePricePrediction with fields predicted_price: float and currency: str = "VND".
    Validate that area_sqm > 0 and bedrooms >= 0 using Field(gt=0) / Field(ge=0) on the request model instead of Query() — this is the equivalent constraint mechanism for request-body fields.

The point of this exercise: swapping the fake formula for model.predict(...) from a real trained model later on is a one-line change inside the function body — everything else (routing, validation, response shaping, docs) stays exactly the same. This is the practical link between what you're building here and your final project's ML backend.
Submission / Self-check

You do not need to submit this separately unless your instructor asks for it — it's meant to deepen the same main.py you already have. Before moving on to Week 8, make sure:

    [ ] PATCH /items/{id} only changes fields actually sent in the body.
    [ ] GET /items correctly combines filtering + sorting + pagination in the right order.
    [ ] Creating a duplicate name returns 409, not 201 or 500.
    [ ] GET /items now returns an envelope (items, total, skip, limit), not a bare array — check /docs to confirm the schema changed.
    [ ] /predict/house-price rejects area_sqm <= 0 with a 422, without any manual if check in the function body.

