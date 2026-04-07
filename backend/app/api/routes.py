from fastapi import APIRouter

from app.schemas.requests import (
    AvatarGenerationRequest,
    DesignPromptRequest,
    OrderCreateRequest,
    VariationRequest,
)
from app.services.avatar import AvatarScalingService
from app.services.design_prompt import DesignPromptService
from app.services.variation_engine import VariationEngine

router = APIRouter()

CATEGORY_COLLECTIONS = {
    "women": ["Saree", "Chudi / Salwar", "Anarkali", "Crop Top", "Jeans", "Kurtha", "Half Saree"],
    "men": ["Shirt", "Pant", "Jeans", "Dhothi", "Paijama", "T-Shirt"],
    "kids": ["Shirts", "Gowns", "Tops", "Little Saree", "Little Dhothi"],
}


@router.get("/categories")
def categories() -> list[str]:
    return list(CATEGORY_COLLECTIONS.keys())


@router.get("/collections/{category}")
def collections(category: str) -> list[str]:
    return CATEGORY_COLLECTIONS.get(category.lower(), [])


@router.post("/avatar/generate")
def generate_avatar(payload: AvatarGenerationRequest) -> dict:
    return AvatarScalingService.to_scaling_payload(payload.measurements)


@router.post("/designs/variations")
def generate_variations(payload: VariationRequest) -> dict:
    variations = VariationEngine.generate(payload)
    return {"count": len(variations), "variations": variations}


@router.post("/designs/prompt")
def prompt_to_json(payload: DesignPromptRequest) -> dict:
    return DesignPromptService.parse(payload.prompt)


@router.post("/orders")
def create_order(payload: OrderCreateRequest) -> dict:
    # DB persistence intentionally abstracted for pluggable repositories.
    return {
        "order_id": f"SS-{payload.user_phone[-4:]}-{payload.items_count:04d}",
        "status": "placed",
        "contact": payload.user_name,
    }
