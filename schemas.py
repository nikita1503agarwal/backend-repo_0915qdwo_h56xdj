"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import date

# Example schemas (you can keep or remove later)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Cafe-specific schemas

class MenuItem(BaseModel):
    """
    Cafe menu items
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price")
    category: str = Field(..., description="Category such as Coffee, Tea, Pastry")
    image_url: Optional[str] = Field(None, description="Image URL")
    is_featured: bool = Field(False, description="Show as featured")

class Reservation(BaseModel):
    """
    Cafe reservations
    Collection name: "reservation"
    Use aliases so the API accepts {"date": ..., "time": ...} from the frontend
    while avoiding name clashes with Python's datetime.date type.
    """
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., description="Guest name")
    email: EmailStr = Field(..., description="Guest email")
    phone: str = Field(..., description="Contact number")
    reservation_date: date = Field(..., alias="date", description="Reservation date")
    reservation_time: str = Field(..., alias="time", description="Time, e.g., 18:30")
    guests: int = Field(..., ge=1, le=20, description="Number of guests")
    message: Optional[str] = Field(None, description="Additional notes")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
