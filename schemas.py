"""
Database Schemas for Flori Mart

Each Pydantic model represents a MongoDB collection (collection name = lowercase class name).
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr


class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Detailed description")
    price: float = Field(..., ge=0, description="Price in USD")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    occasion: Optional[str] = Field(None, description="Occasion category")
    style: Optional[str] = Field(None, description="Style tag")
    color: Optional[str] = Field(None, description="Dominant color")
    sizes: List[str] = Field(default_factory=lambda: ["S","M","L"], description="Available size options")
    is_featured: bool = Field(False, description="Featured on homepage")
    rating: float = Field(0, ge=0, le=5, description="Average rating")
    rating_count: int = Field(0, ge=0, description="Number of ratings")


class Review(BaseModel):
    product_id: str = Field(..., description="Related product id")
    name: str = Field(..., description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating 1-5")
    comment: Optional[str] = Field(None, description="Review text")


class Newsletter(BaseModel):
    email: EmailStr
    source: Optional[str] = Field(None)


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str


class OrderItem(BaseModel):
    product_id: str
    title: str
    price: float
    quantity: int = Field(..., ge=1)
    size: Optional[str] = None
    image: Optional[str] = None


class Address(BaseModel):
    full_name: str
    phone: str
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str


class Order(BaseModel):
    items: List[OrderItem]
    subtotal: float = Field(..., ge=0)
    delivery_fee: float = Field(0, ge=0)
    total: float = Field(..., ge=0)
    email: EmailStr
    shipping_address: Address
    payment_method: Literal["card", "cod", "bank"] = "cod"
    notes: Optional[str] = None
