import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Product, Review, Newsletter, ContactMessage, Order

app = FastAPI(title="Flori Mart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"name": "Flori Mart API", "message": "Welcome to nature's boutique"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "Unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# Products
@app.post("/api/products", response_model=dict)
def create_product(product: Product):
    try:
        product_id = create_document("product", product)
        return {"id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products", response_model=List[dict])
def list_products(occasion: Optional[str] = None, style: Optional[str] = None, color: Optional[str] = None, featured: Optional[bool] = None):
    try:
        q = {}
        if occasion:
            q["occasion"] = occasion
        if style:
            q["style"] = style
        if color:
            q["color"] = color
        if featured is not None:
            q["is_featured"] = featured
        products = get_documents("product", q)
        # Convert ObjectId to string
        for p in products:
            p["id"] = str(p.pop("_id"))
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/{product_id}", response_model=dict)
def get_product(product_id: str):
    try:
        from bson import ObjectId
        item = db["product"].find_one({"_id": ObjectId(product_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Product not found")
        item["id"] = str(item.pop("_id"))
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Reviews
@app.post("/api/reviews", response_model=dict)
def add_review(review: Review):
    try:
        review_id = create_document("review", review)
        return {"id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reviews/{product_id}", response_model=List[dict])
def get_reviews(product_id: str):
    try:
        reviews = get_documents("review", {"product_id": product_id})
        for r in reviews:
            r["id"] = str(r.pop("_id"))
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Newsletter
@app.post("/api/newsletter", response_model=dict)
def subscribe(newsletter: Newsletter):
    try:
        sub_id = create_document("newsletter", newsletter)
        return {"id": sub_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Contact
@app.post("/api/contact", response_model=dict)
def contact(message: ContactMessage):
    try:
        msg_id = create_document("contactmessage", message)
        return {"id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Orders / Checkout
@app.post("/api/orders", response_model=dict)
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
