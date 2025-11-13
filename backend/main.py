from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import db, create_document, get_documents
from schemas import MenuItem, Reservation

app = FastAPI(title="Cafe API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test_db():
    info = {
        "database": str(db.name),
        "time": datetime.utcnow().isoformat(),
    }
    return {"status": "ok", "info": info}


@app.get("/api/menu", response_model=List[MenuItem])
async def get_menu():
    items = await get_documents("menuitem", {}, limit=100)  # collection from class name lowercased
    # if empty, return a friendly default
    if not items:
        return [
            MenuItem(
                name="Signature Latte",
                description="Velvety espresso with house-made syrup",
                price=4.5,
                category="Coffee",
                image_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
                is_featured=True,
            ),
            MenuItem(
                name="Croissant",
                description="Buttery flaky pastry, baked daily",
                price=3.0,
                category="Bakery",
                image_url="https://images.unsplash.com/photo-1519681393784-d120267933ba",
                is_featured=False,
            ),
        ]
    # coerce raw docs into pydantic models
    return [MenuItem(**{k: v for k, v in doc.items() if k != "_id"}) for doc in items]


@app.post("/api/reservations")
async def create_reservation(payload: Reservation):
    # convert to dict respecting aliases so API can accept {date, time}
    data = payload.model_dump(by_alias=True)
    data["created_at"] = datetime.utcnow().isoformat()

    try:
        inserted_id = await create_document("reservation", data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "id": str(inserted_id)}
