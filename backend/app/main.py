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

@app.post("/orders")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    # 1. Check customer exists
    customer = db.query(Customer).filter(
        Customer.id == order.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # 2. Validate stock first (IMPORTANT)
    for item in order.items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

    # 3. Create order
    new_order = Order(customer_id=order.customer_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).all()

    result = []

    for order in orders:

        items_list = []
        total = 0

        for item in order.items:

            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            item_total = product.price * item.quantity

            total += item_total

            items_list.append({
                "product_name": product.name,
                "sku": product.sku,
                "quantity": item.quantity,
                "price": product.price,
                "subtotal": item_total
            })

        result.append({
            "order_id": order.id,
            "customer_id": order.customer_id,
            "customer_name": order.customer.name,
            "items": items_list,
            "total_amount": total
        })

    return result    

    # 4. Create order items + reduce stock
    for item in order.items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(order_item)

        # reduce stock
        product.stock_quantity -= item.quantity

    # 5. Save everything
    db.commit()

    return {
        "message": "Order created successfully",
        "order_id": new_order.id
    }