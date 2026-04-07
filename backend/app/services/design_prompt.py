class DesignPromptService:
    """Very small NLP helper for prompt-to-json customization."""

    @staticmethod
    def parse(prompt: str) -> dict:
        lowered = prompt.lower()
        payload = {"color": None, "remove": [], "add": []}

        colors = ["red", "yellow", "blue", "green", "black", "white", "pink", "gold"]
        for color in colors:
            if color in lowered:
                payload["color"] = color
                break

        removable = ["border", "embroidery", "sleeve", "pallu", "neck"]
        for item in removable:
            if f"remove {item}" in lowered or f"without {item}" in lowered:
                payload["remove"].append(item)

        additions = ["waist design", "border", "embroidery", "sleeve", "pallu", "neck"]
        for item in additions:
            if f"add {item}" in lowered:
                payload["add"].append(item.replace(" ", "_"))

        return payload
