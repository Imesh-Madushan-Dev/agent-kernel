"""Business logic for the Farmer Advisor agents. Pure functions over local JSON data.

ponytail: local JSON knowledge base; swap the loaders for real APIs when available.
"""

import json
from pathlib import Path

_DATA = Path(__file__).parent / "data"


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


def get_price(crop: str, market: str = "") -> dict:
    """Get the current market price for a crop.

    :param crop: crop name, e.g. "rice", "tomato"
    :param market: optional market name (Pettah, Dambulla, Kandy); empty returns all markets
    """
    data = json.loads((_DATA / "market_prices.sample.json").read_text(encoding="utf-8"))
    prices = data["prices"].get(crop.lower().strip())
    if prices is None:
        return {"error": f"No price data for '{crop}'. Available: {list(data['prices'])}"}
    if market:
        match = next((m for m in prices if m.lower() == market.lower().strip()), None)
        if match is None:
            return {"error": f"No data for market '{market}'. Available: {list(prices)}"}
        prices = {match: prices[match]}
    return {"crop": crop.lower().strip(), "prices": prices, "unit": f"{data['currency']}/{data['unit']}", "as_of": data["as_of"]}


def get_forecast(location: str) -> dict:
    """Get a 3-day weather forecast for a location.

    :param location: town or district name, e.g. "Kandy"
    ponytail: deterministic mock keyed on location hash; swap for a real weather API (e.g. open-meteo) when a key/network is available.
    """
    conditions = ["sunny", "partly cloudy", "light rain", "heavy rain", "windy"]
    seed = sum(ord(c) for c in location.lower().strip())
    days = []
    for i, day in enumerate(["today", "tomorrow", "day after"]):
        cond = conditions[(seed + i * 3) % len(conditions)]
        days.append({"day": day, "condition": cond, "temp_c": 24 + (seed + i) % 8, "rain_chance_pct": {"sunny": 5, "partly cloudy": 20, "light rain": 60, "heavy rain": 90, "windy": 15}[cond]})
    return {"location": location.strip().title(), "forecast": days}


if __name__ == "__main__":  # self-check
    d = diagnose_from_symptoms("rice", "I see gray spots on leaves and dried leaf tips")
    assert d["disease"] == "Rice Blast", d
    assert diagnose_from_symptoms("rice", "purple polka dots")["disease"] in ("unknown", "Rice Blast")
    assert "treatment" in get_treatment("late_blight")
    assert "error" in get_treatment("nope")
    p = get_price("tomato", "pettah")
    assert p["prices"] == {"Pettah": 340}, p
    assert "error" in get_price("durian")
    f = get_forecast("Kandy")
    assert len(f["forecast"]) == 3 and f == get_forecast("kandy "), f
    print("tools self-check OK")
