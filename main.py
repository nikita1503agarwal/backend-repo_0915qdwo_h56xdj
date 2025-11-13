import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import create_document, get_documents
from schemas import MenuItem, Reservation

app = FastAPI(title="Cafe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Cafe API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Welcome to our cafe!"}

# Public endpoints
@app.get("/api/menu", response_model=List[MenuItem])
def list_menu():
    try:
        docs = get_documents("menuitem")
        # Convert ObjectId and datetime to strings if present
        for d in docs:
            d["id"] = str(d.get("_id"))
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])  # not in schema but safe
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"])  # not in schema but safe
        # Coerce to schema shape
        return [MenuItem(**{k: v for k, v in d.items() if k in MenuItem.model_fields}) for d in docs]
    except Exception as e:
        # If DB not available, return a curated sample menu
        sample = [
            MenuItem(name="Iced Latte", description="Espresso with cold milk and ice", price=3.5, category="Coffee", image_url=None, is_featured=True),
            MenuItem(name="Matcha Latte", description="Ceremonial grade matcha with milk", price=4.0, category="Tea", image_url=None, is_featured=True),
            MenuItem(name="Butter Croissant", description="Flaky, baked fresh daily", price=2.2, category="Pastry", image_url=None, is_featured=False),
            MenuItem(name="Mocha", description="Chocolate and espresso harmony", price=3.8, category="Coffee", image_url=None, is_featured=False),
        ]
        return sample

@app.post("/api/reservations")
def create_reservation(res: Reservation):
    try:
        doc_id = create_document("reservation", res)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        # Fallback: accept but mark as not persisted
        return {"status": "accepted", "id": None}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
