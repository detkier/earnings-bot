import requests
from datetime import date, timedelta
from config import FMP_API_KEY, WATCHLIST, COMPANY_NAMES


def fetch_next_week_calendar() -> list[dict]:
    """抓下週會公布財報的重點公司（週一到週五）。"""
    today = date.today()
    # 下週一
    days_until_monday = (7 - today.weekday()) % 7 or 7
    from_date = today + timedelta(days=days_until_monday)
    to_date = from_date + timedelta(days=4)  # 週一到週五

    url = (
        f"https://financialmodelingprep.com/stable/earnings-calendar"
        f"?from={from_date}&to={to_date}&apikey={FMP_API_KEY}"
    )
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"calendar API error: {e}")
        return []

    results = []
    seen = set()
    for item in data:
        symbol = item.get("symbol", "")
        if symbol not in WATCHLIST or symbol in seen:
            continue
        seen.add(symbol)
        results.append({
            "symbol": symbol,
            "name": COMPANY_NAMES.get(symbol, symbol),
            "date": item.get("date", ""),
            "eps_est": item.get("epsEstimated"),
            "rev_est": item.get("revenueEstimated"),
        })

    results.sort(key=lambda x: x["date"])
    return results, from_date, to_date
