import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from farmer_advisor.tools import diagnose_from_symptoms, get_forecast, get_price, get_treatment


def test_diagnose_known_disease():
    result = diagnose_from_symptoms("rice", "gray spots on leaves and dried leaf tips")
    assert result["disease"] == "Rice Blast"
    assert {"confidence", "treatment", "prevention"} <= result.keys()


def test_diagnose_unknown_symptoms():
    assert "message" in diagnose_from_symptoms("mango", "nothing visible")


def test_get_treatment():
    assert "treatment" in get_treatment("late_blight")
    assert "error" in get_treatment("bogus")


def test_get_price_with_market():
    result = get_price("tomato", "pettah")
    assert result["prices"] == {"Pettah": 340}
    assert result["unit"] == "LKR/kg"


def test_get_price_all_markets():
    assert len(get_price("rice")["prices"]) == 3


def test_get_price_unknown_crop():
    assert "error" in get_price("durian")


def test_forecast_real_or_graceful():
    result = get_forecast("Kandy")
    assert "error" in result or (len(result["forecast"]) == 3 and result["source"] == "open-meteo.com")


def test_forecast_unknown_location():
    assert "error" in get_forecast("xyzzy-not-a-place")
