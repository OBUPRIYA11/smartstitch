from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    role: str = Field(pattern="^(public|garment)$")
    full_name: str
    email: EmailStr
    phone: str


class UserOut(BaseModel):
    id: int
    role: str
    full_name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True


class Measurements(BaseModel):
    chest: float
    waist: float
    hip: float
    shoulder: float
    sleeve: float
    inseam: float
    height: float


class ModelGenerateRequest(BaseModel):
    user_id: int
    category: str
    design: str
    material: str
    color: str
    skin_tone: str
    measurements: Measurements
    prompt: str | None = None


class OrderCreate(BaseModel):
    user_id: int
    dress_category: str
    dress_design: str
    material: str
    color: str
    measurements: Measurements
    shipping_address: str
    extra_details: str = ""


class OrderOut(BaseModel):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
