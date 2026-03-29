import requests
from datetime import date, timedelta
from calendar import monthrange
from config import FMP_API_KEY, WATCHLIST, COMPANY_NAMES


def fetch_next_month_calendar() -> list[dict]:
    """抓下個月會公布財報的重點公司。"""
    today = date.today()
    # 計算下個月的起訖日
    if today.month == 12:
        year, month = today.year + 1, 1
    else:
        year, month = today.year, today.month + 1
    from_date = date(year, month, 1)
    to_date = date(year, month, monthrange(year, month)[1])

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
    return results
