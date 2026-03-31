from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, Payment, User
from app.mongo import model_collection
from app.schemas import ModelGenerateRequest, OrderCreate, OrderOut, UserCreate, UserOut
from app.services.notifier import notify_order
from app.services.recommendation import recommend_colors

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        return existing
    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/catalog")
def catalog():
    return {
        "women": ["Blazer Set", "Evening Gown", "Kurti", "Casual Suit"],
        "men": ["Business Suit", "Sherwani", "Tuxedo", "Casual Jacket"],
        "kids": ["Mini Suit", "Frock", "School Formal", "Party Dress"],
    }


@router.get("/skin-tone/{skin_tone}/recommendations")
def color_recommendations(skin_tone: str):
    return {"skin_tone": skin_tone, "recommended_colors": recommend_colors(skin_tone)}


@router.post("/models/generate")
def generate_models(payload: ModelGenerateRequest):
    base_scale = payload.measurements.height / 170
    models = []
    for idx in range(1, 21):
        model = {
            "model_id": f"model-{idx}",
            "label": f"{payload.design} Variant {idx}",
            "design_seed": idx,
            "body_scale": round(base_scale * (0.9 + idx * 0.01), 2),
            "color": payload.color,
            "material": payload.material,
            "category": payload.category,
            "prompt": payload.prompt,
            "created_at": datetime.utcnow().isoformat(),
        }
        models.append(model)

    model_collection.insert_one(
        {
            "user_id": payload.user_id,
            "design": payload.design,
            "models": models,
            "input": payload.model_dump(mode="json"),
            "created_at": datetime.utcnow(),
        }
    )

    return {"models": models, "webxr_supported": True}


@router.post("/orders", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        user_id=payload.user_id,
        dress_category=payload.dress_category,
        dress_design=payload.dress_design,
        material=payload.material,
        color=payload.color,
        measurements=payload.measurements.model_dump(),
        shipping_address=payload.shipping_address,
        extra_details=payload.extra_details,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    notify_order(order.id, f"{order.dress_category} / {order.dress_design} / {order.color}")
    return order


@router.get("/garment/dashboard")
def garment_dashboard(db: Session = Depends(get_db)):
    statuses = [
        "placed",
        "in_process",
        "stitching",
        "completed",
        "about_to_deliver",
        "delivered",
    ]

    counts = {
        status: db.query(func.count(Order.id)).filter(Order.status == status).scalar() for status in statuses
    }
    payments = db.query(Payment).all()
    return {
        "status_counts": counts,
        "payments": [
            {
                "order_id": p.order_id,
                "amount": p.amount,
                "mode": p.mode,
                "account_ref": p.account_ref,
                "paid_at": p.paid_at.isoformat(),
            }
            for p in payments
        ],
    }


@router.get("/garment/orders")
def garment_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "category": o.dress_category,
            "design": o.dress_design,
            "material": o.material,
            "color": o.color,
            "status": o.status,
            "measurements": o.measurements,
            "address": o.shipping_address,
            "created_at": o.created_at.isoformat(),
        }
        for o in orders
    ]
