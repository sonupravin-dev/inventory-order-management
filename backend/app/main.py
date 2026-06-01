from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import (
    Base,
    Product,
    Customer,
    Order,
    OrderItem
)
from .schemas import (
    ProductCreate,
    ProductResponse,
    CustomerCreate,
    CustomerResponse,
    OrderCreate
)


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Inventory Management API"}


@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    existing = db.query(Product).filter(Product.sku == product.sku).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    new_product = Product(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/customers", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_customer = Customer(**customer.dict())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).all()

    result = []

    for order in orders:
        items_list = []
        total = 0

        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()

            subtotal = product.price * item.quantity
            total += subtotal

            items_list.append({
                "product_name": product.name,
                "sku": product.sku,
                "quantity": item.quantity,
                "price": product.price,
                "subtotal": subtotal
            })

        result.append({
            "order_id": order.id,
            "customer_name": order.customer.name,
            "items": items_list,
            "total_amount": total
        })

    return result