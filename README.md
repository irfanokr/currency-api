# Free Currency Exchange Rates API

**170+ currencies · Any base currency · No API key · No rate limits · Daily updated**

> Maintained by [irfanokr](https://github.com/irfanokr) &nbsp;·&nbsp; Free forever

---

## Why Use This?

| Feature | This API | Fixer.io | Open Exchange Rates |
|---|---|---|---|
| Free | ✅ | ❌ (paid) | ❌ (limited free) |
| No API key | ✅ | ❌ | ❌ |
| No rate limits | ✅ | ❌ | ❌ |
| Any base currency | ✅ | ❌ (USD only on free) | ❌ (USD only on free) |
| Historical data | ✅ | ❌ (paid) | ❌ (paid) |
| Open source | ✅ | ❌ | ❌ |

---

## Quick Start

No signup. No API key. Just GET the URL.

### Get all rates for any base currency

```
GET https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/{base}.json
```

**Examples:**

```bash
# USD as base — get all currencies priced in USD
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/usd.json

# EUR as base
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/eur.json

# PKR as base — get all currencies priced in Pakistani Rupees
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/pkr.json

# SAR as base — Saudi Riyal
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/sar.json
```

### Get a specific date (historical)

```bash
# Replace 'latest' with a date: YYYY.M.D (npm version format)
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@2026.4.29/v1/currencies/usd.json
```

### Get all currencies list

```bash
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/currencies.json
```

---

## Response Format

```json
{
  "date": "2026-04-29",
  "attribution": "irfanokr | https://github.com/irfanokr/currency-api | Free, no-limit currency API",
  "usd": {
    "aed": 3.6725,
    "aud": 1.5821,
    "btc": 0.0000129,
    "cny": 7.2541,
    "eur": 0.8540,
    "gbp": 0.7399,
    "inr": 83.942,
    "jpy": 159.61,
    "pkr": 278.50,
    "sar": 3.7501,
    "try": 38.42,
    "...": "170+ more currencies"
  }
}
```

### Minified version (faster, smaller)

Add `.min.json` instead of `.json`:

```bash
curl https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/usd.min.json
```

---

## Currency Conversion Formula

To convert **100 USD → PKR**:

```js
const base = await fetch('https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/usd.json')
  .then(r => r.json());

const pkrRate = base.usd.pkr;       // e.g. 278.50
const result  = 100 * pkrRate;      // 27850 PKR
```

To convert **PKR → USD** (or any pair):

```js
const base = await fetch('https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/pkr.json')
  .then(r => r.json());

const usdRate = base.pkr.usd;       // e.g. 0.003590
const result  = 50000 * usdRate;    // 179.5 USD
```

---

## All Endpoints

| Endpoint | Description |
|---|---|
| `/v1/currencies/currencies.json` | List of all supported currency codes |
| `/v1/currencies/{base}.json` | All rates with `{base}` as the base currency |
| `/v1/currencies/{base}.min.json` | Minified version of the above |
| `/v1/currencies/latest.json` | All bases × all targets in one file |

---

## Supported Currencies (170+)

Includes all major **fiat currencies**, top **cryptocurrencies** (BTC, ETH, USDT, BNB…), and **precious metals** (XAU, XAG).

Currencies relevant to Pakistan & remittance corridors:

| Code | Currency |
|---|---|
| PKR | Pakistani Rupee |
| USD | US Dollar |
| SAR | Saudi Riyal |
| AED | UAE Dirham |
| GBP | British Pound |
| EUR | Euro |
| CNY | Chinese Yuan |
| MYR | Malaysian Ringgit |
| QAR | Qatari Rial |
| KWD | Kuwaiti Dinar |
| BHD | Bahraini Dinar |
| OMR | Omani Rial |

---

## Use in Your Project

### JavaScript / Node.js

```js
async function convert(amount, from, to) {
  const url = `https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/${from.toLowerCase()}.min.json`;
  const data = await fetch(url).then(r => r.json());
  return amount * data[from.toLowerCase()][to.toLowerCase()];
}

// 100 USD to PKR
convert(100, 'usd', 'pkr').then(console.log);  // 27850
```

### Python

```python
import urllib.request, json

def convert(amount, from_currency, to_currency):
    url = f"https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/{from_currency}.min.json"
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    return amount * data[from_currency][to_currency]

print(convert(100, "usd", "pkr"))  # 27850.0
```

### PHP

```php
function convert($amount, $from, $to) {
    $url = "https://cdn.jsdelivr.net/npm/@irfanokr/currency-api@latest/v1/currencies/{$from}.min.json";
    $data = json_decode(file_get_contents($url), true);
    return $amount * $data[$from][$to];
}

echo convert(100, 'usd', 'pkr');  // 27850
```

---

## Fallback URL

If jsDelivr is down, use the GitHub raw URL:

```
https://raw.githubusercontent.com/irfanokr/currency-api/main/v1/currencies/{base}.json
```

---

## How It Works

1. **GitHub Actions** runs daily at midnight UTC
2. **Python script** fetches rates from multiple free data sources
3. Generates **one JSON file per base currency** (170+ files)
4. Publishes as an **npm package** (`@irfanokr/currency-api`)
5. **jsDelivr CDN** serves the files globally — no server needed, ever

**Zero cost. Zero maintenance. Open source.**

---

## Attribution

If you use this API in your project, a credit in your README or app is appreciated:

```markdown
Exchange rates by [irfanokr/currency-api](https://github.com/irfanokr/currency-api) — Free & open source
```

---

## License

[Unlicense](LICENSE) — public domain. Use it however you want.

---

*Maintained by [irfanokr](https://github.com/irfanokr)*
