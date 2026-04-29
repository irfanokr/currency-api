"""
Free Currency Exchange Rates API
Fetches daily rates and generates one JSON file per currency.
Runs via GitHub Actions daily — zero server required.
Maintained by irfanokr | https://github.com/irfanokr
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Data sources (all free, no key required) ──────────────────────────────────
SOURCES = [
    "https://open.er-api.com/v6/latest/USD",           # primary
    "https://api.exchangerate-api.com/v4/latest/USD",   # fallback 1
    "https://api.frankfurter.app/latest?from=USD",      # fallback 2 (ECB, ~30 currencies)
]

ATTRIBUTION = "irfanokr | https://github.com/irfanokr/currency-api | Free, no-limit currency API"

OUTPUT_DIR = Path("v1/currencies")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_usd_rates() -> dict:
    """Fetch USD-based rates from the first available source."""
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "currency-api/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())

            # Normalise response shape across sources
            if "rates" in data:
                rates = data["rates"]
            elif "conversion_rates" in data:
                rates = data["conversion_rates"]
            else:
                continue

            # Ensure USD = 1.0 as anchor
            rates["USD"] = 1.0
            rates = {k.lower(): round(v, 10) for k, v in rates.items() if isinstance(v, (int, float))}
            print(f"Fetched {len(rates)} currencies from {url}")
            return rates

        except Exception as e:
            print(f"Source failed ({url}): {e}")

    raise RuntimeError("All data sources failed.")


def compute_cross_rates(usd_rates: dict, base: str) -> dict:
    """Given USD-based rates, compute rates for any base currency."""
    if base not in usd_rates:
        return {}
    base_in_usd = usd_rates[base]          # how many USD = 1 base
    cross = {}
    for code, usd_val in usd_rates.items():
        # base → code:  1 base = (usd_val / base_in_usd) code
        cross[code] = round(usd_val / base_in_usd, 10)
    return cross


def write_json(path: Path, data: dict):
    pretty = json.dumps(data, indent=2, ensure_ascii=False)
    minified = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    path.write_text(pretty, encoding="utf-8")
    path.with_suffix(".min.json").write_text(minified, encoding="utf-8")


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Generating rates for {today}...")

    usd_rates = fetch_usd_rates()
    all_currencies = sorted(usd_rates.keys())

    # 1. Write currencies list
    currencies_list = {c: c.upper() for c in all_currencies}
    write_json(OUTPUT_DIR / "currencies.json",
               {"date": today, "attribution": ATTRIBUTION, "currencies": currencies_list})

    # 2. Write one file per base currency
    for base in all_currencies:
        cross = compute_cross_rates(usd_rates, base)
        if not cross:
            continue
        payload = {
            "date": today,
            "attribution": ATTRIBUTION,
            base: cross,
        }
        write_json(OUTPUT_DIR / f"{base}.json", payload)

    # 3. Write combined latest.json (all bases, all targets)
    combined = {"date": today, "attribution": ATTRIBUTION, "rates": {}}
    for base in all_currencies:
        combined["rates"][base] = compute_cross_rates(usd_rates, base)
    write_json(OUTPUT_DIR / "latest.json", combined)

    print(f"Done. Generated {len(all_currencies)} currency files.")


if __name__ == "__main__":
    main()
