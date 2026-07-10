"""Self-check: python -m farmer_advisor.tools"""

from . import diagnose_from_symptoms, get_forecast, get_price, get_treatment

d = diagnose_from_symptoms("rice", "I see gray spots on leaves and dried leaf tips")
assert d["disease"] == "Rice Blast", d
assert diagnose_from_symptoms("rice", "purple polka dots")["disease"] in ("unknown", "Rice Blast")
assert "treatment" in get_treatment("late_blight")
assert "error" in get_treatment("nope")
p = get_price("tomato", "pettah")
assert p["prices"] == {"Pettah": 340}, p
assert "error" in get_price("durian")
f = get_forecast("Kandy")
assert "error" in f or len(f["forecast"]) == 3, f
assert "error" in get_forecast("xyzzy-not-a-place")
print("tools self-check OK")
