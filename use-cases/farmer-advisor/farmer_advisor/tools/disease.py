"""Crop-disease diagnosis tools. Pure functions over the local JSON knowledge base.

ponytail: local JSON knowledge base; swap the loaders for real APIs when available.
"""

import json
from pathlib import Path

_DATA = Path(__file__).parents[1] / "data"


def _diseases() -> list[dict]:
    return json.loads((_DATA / "crop_diseases.json").read_text(encoding="utf-8"))


def diagnose_from_symptoms(crop: str, symptoms: str) -> dict:
    """Diagnose a crop disease from described symptoms.

    :param crop: crop name, e.g. "rice", "tomato"
    :param symptoms: farmer's description of what they see on the plant
    :return: dict with disease, confidence, treatment, prevention (or a not-found message)
    """
    words = set(symptoms.lower().split())
    best, best_score = None, 0
    for entry in _diseases():
        if crop.lower().strip() not in entry["crop"]:
            continue
        score = sum(1 for s in entry["symptoms"] for w in s.split() if w in words)
        if score > best_score:
            best, best_score = entry, score
    if best is None:
        return {"disease": "unknown", "message": f"No match for '{crop}' with those symptoms. Ask the farmer for more details (spots, color, affected part)."}
    return {
        "disease": best["disease"],
        "confidence": "high" if best_score >= 3 else "medium" if best_score >= 2 else "low",
        "treatment": best["treatment"],
        "prevention": best["prevention"],
    }


def get_treatment(disease_id: str) -> dict:
    """Get treatment and prevention advice for a known disease id.

    :param disease_id: id such as "rice_blast", "late_blight"
    """
    for entry in _diseases():
        if entry["id"] == disease_id:
            return {"disease": entry["disease"], "treatment": entry["treatment"], "prevention": entry["prevention"]}
    return {"error": f"Unknown disease id '{disease_id}'. Known: {[e['id'] for e in _diseases()]}"}
