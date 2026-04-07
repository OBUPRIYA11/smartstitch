from app.schemas.requests import Measurements


class AvatarScalingService:
    """Converts manual body measurements into normalized scaling for 3D rigs."""

    @staticmethod
    def _ratio(value: float, baseline: float) -> float:
        return round(value / baseline, 3)

    @classmethod
    def to_scaling_payload(cls, m: Measurements) -> dict:
        return {
            "global_scale": cls._ratio(m.height_cm, 170),
            "torso_width_scale": cls._ratio((m.chest_cm + m.waist_cm + m.hip_cm) / 3, 90),
            "shoulder_scale": cls._ratio(m.shoulder_cm, 42),
            "arm_bone_scale": cls._ratio(m.arm_length_cm, 60),
            "leg_bone_scale": cls._ratio(m.leg_length_cm, 90),
            "wrist_scale": cls._ratio(m.wrist_cm, 17),
            "thigh_scale": cls._ratio(m.thigh_cm, 52),
            "ankle_scale": cls._ratio(m.ankle_cm or 23, 23),
            "raw_measurements": m.model_dump(),
        }
