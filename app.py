from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="WeldBidPro API", version="1.0.0")


# ----------------------------
# Data Models
# ----------------------------
class Material(BaseModel):
    name: str
    quantity: float
    unit_cost: float


class Consumable(BaseModel):
    name: str
    quantity: float
    unit_cost: float


class EstimateRequest(BaseModel):
    labor_hours: float
    labor_rate: float
    materials: List[Material]
    consumables: Optional[List[Consumable]] = []
    markup_percent: float = 0.0
    tax_percent: float = 0.0


class EstimateResponse(BaseModel):
    subtotal: float
    markup: float
    tax: float
    total: float


# ----------------------------
# Routes
# ----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "WeldBidPro API running"}


@app.post("/estimate/calc", response_model=EstimateResponse)
def calculate_estimate(req: EstimateRequest):
    # Labor cost
    labor_cost = req.labor_hours * req.labor_rate

    # Materials cost
    material_cost = sum(m.quantity * m.unit_cost for m in req.materials)

    # Consumables cost
    consumable_cost = sum(c.quantity * c.unit_cost for c in req.consumables)

    subtotal = labor_cost + material_cost + consumable_cost

    # Markup
    markup = subtotal * (req.markup_percent / 100)

    # Tax
    taxable_amount = subtotal + markup
    tax = taxable_amount * (req.tax_percent / 100)

    total = subtotal + markup + tax

    return {
        "subtotal": round(subtotal, 2),
        "markup": round(markup, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
    }


@app.get("/price-intel/compare")
def compare_prices():
    """
    Placeholder endpoint for supplier price index comparisons.
    Later, this will accept part numbers/materials
    and return cheaper supplier suggestions.
    """
    return {"message": "Supplier price comparison coming soon."}
