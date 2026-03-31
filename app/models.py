from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[str] = mapped_column(String(20), default="public")
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(20))


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    dress_category: Mapped[str] = mapped_column(String(50))
    dress_design: Mapped[str] = mapped_column(String(120))
    material: Mapped[str] = mapped_column(String(120))
    color: Mapped[str] = mapped_column(String(20))
    measurements: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(30), default="placed")
    shipping_address: Mapped[str] = mapped_column(Text)
    extra_details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, index=True)
    amount: Mapped[float] = mapped_column(Float)
    mode: Mapped[str] = mapped_column(String(50))
    account_ref: Mapped[str] = mapped_column(String(80))
    paid_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
