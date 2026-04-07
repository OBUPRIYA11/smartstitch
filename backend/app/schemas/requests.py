from pydantic import BaseModel, Field


class Measurements(BaseModel):
    height_cm: float = Field(gt=80, lt=260)
    neck_cm: float = Field(gt=20, lt=70)
    shoulder_cm: float = Field(gt=20, lt=80)
    chest_cm: float = Field(gt=40, lt=180)
    waist_cm: float = Field(gt=30, lt=180)
    hip_cm: float = Field(gt=40, lt=200)
    arm_length_cm: float = Field(gt=20, lt=100)
    wrist_cm: float = Field(gt=10, lt=40)
    leg_length_cm: float = Field(gt=30, lt=140)
    thigh_cm: float = Field(gt=20, lt=100)
    ankle_cm: float | None = Field(default=None, gt=10, lt=50)


class AvatarGenerationRequest(BaseModel):
    measurements: Measurements


class VariationRequest(BaseModel):
    category: str
    dress_type: str
    color: str
    fabric: str
    requested_count: int = Field(default=6, ge=3, le=20)
    reference_features: dict[str, str] | None = None


class DesignPromptRequest(BaseModel):
    prompt: str


class OrderCreateRequest(BaseModel):
    user_name: str
    user_phone: str
    address: str
    notes: str | None = None
    items_count: int = Field(ge=1, le=99)
