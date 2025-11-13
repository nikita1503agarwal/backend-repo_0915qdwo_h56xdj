from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class MenuItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None
    is_featured: bool = False


class Reservation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    full_name: str = Field(..., description="Customer full name")
    phone: str = Field(..., description="Contact phone number")
    guests: int = Field(..., ge=1, le=20, description="Number of guests")
    reservation_date: str = Field(..., alias="date", description="YYYY-MM-DD")
    reservation_time: str = Field(..., alias="time", description="HH:MM")
    notes: Optional[str] = None


class MenuResponse(BaseModel):
    items: List[MenuItem]
