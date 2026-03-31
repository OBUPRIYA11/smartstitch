from collections.abc import Sequence

SKIN_TONE_MAP = {
    "fair": ["#1E3A8A", "#2563EB", "#BE123C", "#065F46"],
    "medium": ["#7C3AED", "#0F766E", "#B45309", "#111827"],
    "olive": ["#14532D", "#0F766E", "#4C1D95", "#7F1D1D"],
    "deep": ["#F59E0B", "#0EA5E9", "#10B981", "#E11D48"],
}


def recommend_colors(skin_tone: str) -> Sequence[str]:
    return SKIN_TONE_MAP.get(skin_tone.lower(), ["#334155", "#6366F1", "#0891B2", "#16A34A"])
