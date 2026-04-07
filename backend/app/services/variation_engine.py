from itertools import product

from app.schemas.requests import VariationRequest


class VariationEngine:
    BORDER = ["minimal", "temple", "zari-heavy", "embroidered", "contrast-piping"]
    PATTERN = ["floral", "paisley", "geometric", "mirror-work", "thread-art"]
    TEXTURE = ["matte", "silk-sheen", "woven", "jacquard", "crinkle"]
    SLEEVE = ["sleeveless", "cap", "elbow", "full", "ruffled"]
    PALLU = ["plain-flow", "layered", "panel-pleat", "digital-print", "dual-tone"]
    NECK = ["boat", "sweetheart", "high-neck", "square", "deep-v"]

    @classmethod
    def generate(cls, request: VariationRequest) -> list[dict]:
        reference = request.reference_features or {}
        combos = product(cls.BORDER, cls.PATTERN, cls.TEXTURE, cls.SLEEVE, cls.PALLU, cls.NECK)

        results: list[dict] = []
        for idx, (border, pattern, texture, sleeve, pallu, neck) in enumerate(combos, start=1):
            results.append(
                {
                    "variation_id": f"{request.dress_type[:3].upper()}-{idx:03d}",
                    "category": request.category,
                    "dress_type": request.dress_type,
                    "color": request.color,
                    "fabric": reference.get("fabric", request.fabric),
                    "design": {
                        "border": reference.get("border", border),
                        "pattern": reference.get("pattern", pattern),
                        "texture": reference.get("texture", texture),
                        "sleeve_style": sleeve,
                        "pallu_style": pallu,
                        "neck_design": neck,
                    },
                }
            )
            if len(results) >= request.requested_count:
                break

        return results
