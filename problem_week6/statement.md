
Opened: Thursday, 10 September 2026, 12:00 AM
Due: Thursday, 10 September 2026, 6:15 PM
Week 06 Assignment — Mini House-Price Prediction API

Web Design and Programming — Faculty of Data Science and Artificial Intelligence
Context

Back in Week 2, you built an HTML form that collects house details (area, number of bedrooms, location) to predict a price. At that time the form had no real backend — any "prediction" was either hardcoded or missing entirely.

This week you will build that backend for real, using FastAPI, and connect it to your Week 2 form so the whole pipeline works end to end: form → HTTP request → Python function → HTTP response → price shown on the page.

The prediction formula you'll use is a simplified placeholder, not a trained ML model — the goal of this assignment is the data flow, not prediction accuracy.
Learning Objectives

By completing this assignment you will practice:

    Writing a plain Python function and exposing it as an HTTP endpoint.
    Choosing between required and optional query parameters.
    Testing an API through the auto-generated /docs (Swagger UI).
    Serving a static frontend file directly from FastAPI so frontend and backend share the same origin.
    Calling your own API from JavaScript using fetch().

Prerequisites

    A working virtual environment with fastapi and uvicorn[standard] installed (from Tiết 1).
    Your Week 2 house-price form (house_form.html), including input fields for area, number of bedrooms, and location, plus a result element and a submit button.
    The following project structure:

project/
├── frontend/
│   └── house_form.html
└── backend/
    └── main.py

Tasks
Task 1 — Prediction function (required)

In main.py, write a plain Python function with this exact signature and formula, so that everyone's output is comparable:

def predict_price(area: float, bedrooms: int, location: str) -> float:
    ...

Formula:

    Start from a base price of 500,000,000 VND.
    Add 15,000,000 VND per m² of area.
    Add 50,000,000 VND per bedroom.
    If location (case-insensitive) is "hanoi", multiply the total by 1.3.
    If location (case-insensitive) is "hcmc", multiply the total by 1.25.
    Any other location: no multiplier.
    Round the final result to the nearest million VND.

Verify your function works correctly by calling it directly (e.g. in a Python shell or a temporary print() statement) before moving on.
Task 2 — Expose it as an endpoint (required)

Create a GET /predict endpoint that:

    Accepts area (required, float) and bedrooms (required, int) as query parameters.
    Accepts location (optional, str, default "other") as a query parameter.
    Calls predict_price() and returns a JSON object containing area, bedrooms, location, and predicted_price.
    Uses def, not async def — justify your choice in one sentence in a comment above the function.

Task 3 — Test via /docs and the URL bar (required)

    Run your app with uvicorn main:app --reload from inside backend/.
    Open http://127.0.0.1:8000/docs, expand /predict, and test it with area=80, bedrooms=3, location=hanoi. Record the returned JSON.
    Test the same request directly from the browser's address bar.
    Try calling /predict without location — confirm it still works and explain why.
    Try calling /predict without area — confirm you get a 422 error and explain why.

Task 4 — Serve the frontend from the same origin (required)

Instead of opening house_form.html with Live Server (a different port from your API), mount it directly from FastAPI so both the page and the API run on 127.0.0.1:8000:

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

    Why not just enable CORS? Because your frontend page and your API would then be running on two different origins (ports), and the browser would block the cross-origin request unless the server explicitly allows it — that's what CORS is for. Configuring CORS middleware correctly is covered in Week 8. This week, avoid the problem entirely by serving both from the same origin.

Confirm the page loads at http://127.0.0.1:8000/static/house_form.html.
Task 5 — Connect the form to the API (required)

Update the JavaScript in house_form.html so that submitting the form:

    Reads the area, bedrooms, and location values from the form inputs.
    Calls fetch() on your /predict endpoint using a relative URL (not an absolute one with a hostname — explain why a relative URL works now).
    Awaits and parses the JSON response.
    Displays the predicted_price in a human-readable format (e.g. with thousands separators) somewhere on the page.
    Handles the case where the request fails (e.g. shows an error message instead of crashing).

Demonstrate that this works by watching the Uvicorn terminal log a new request every time you submit the form.
Task 6 — Bonus (optional, not graded)

Add a second endpoint, POST /predict, that accepts the same three fields as a JSON request body instead of query parameters, using a Pydantic model:

from pydantic import BaseModel

class HouseInput(BaseModel):
    area: float
    bedrooms: int
    location: str = "other"

You don't need to fully understand Pydantic yet — this is a preview of Week 7. Just get it working and be ready to explain, in your own words, one difference between sending data via query parameters and sending it via a JSON body.
Deliverables

Submit:

    main.py — containing predict_price(), the GET /predict endpoint, and the StaticFiles mount (Task 6 optional but encouraged).
    house_form.html — updated with the working fetch() call.
    A short README.md (a few sentences) describing:
        How to run your project (commands, in order).
        Your answers to the two "explain why" questions in Task 3.
        Your answer to the "why does a relative URL work" question in Task 5.

Grading Rubric (20 points)
Criterion 	Points
predict_price() matches the specified formula exactly 	4
/predict endpoint has correct required/optional parameters and return shape 	4
Endpoint tested and working via /docs (screenshot or description in README) 	3
StaticFiles mount works — form loads from 127.0.0.1:8000/static/... 	3
Form successfully calls the API and displays the predicted price 	4
Written answers to the "explain why" questions are correct and clear 	2
Bonus: working POST /predict with Pydantic model 	+2
Common Pitfalls to Avoid

    Forgetting type hints on query parameters (area, bedrooms) — you lose automatic validation.
    Placing app.mount(...) before your route decorators instead of after.
    Opening the form through Live Server out of habit instead of through 127.0.0.1:8000/static/... — this will bring back the CORS error this assignment is designed to avoid.
    Forgetting await inside an async def function (if you experiment with making an endpoint async).
    Mismatched field names between the JSON returned by the API and the JavaScript reading data.something.

Submission status
Submission status 	No submissions have been made yet
Grading status 	Not graded
Time remaining 	Assignment is overdue by: 6 days 20 hours