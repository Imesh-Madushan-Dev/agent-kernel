"""Market-price tools. Pure functions over the local JSON price feed.

ponytail: sample JSON price feed; swap the loader for a real market API when available.
"""

import json
from pathlib import Path

_DATA = Path(__file__).parents[1] / "data"


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
