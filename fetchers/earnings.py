import requests
from datetime import date, timedelta
from config import FMP_API_KEY, WATCHLIST, COMPANY_NAMES


def _beat_miss(actual, estimate) -> str:
    if actual is None or estimate is None or estimate == 0:
        return ""
    pct = (actual - estimate) / abs(estimate) * 100
    if pct >= 3:
        return f"✅ 超預期 +{pct:.1f}%"
    elif pct <= -3:
        return f"❌ 低於預期 {pct:.1f}%"
    else:
        return f"➡️ 符合預期 {pct:+.1f}%"


def _fmt_revenue(rev) -> str:
    if rev is None:
        return "N/A"
    if rev >= 1e12:
        return f"${rev/1e12:.2f}T"
    elif rev >= 1e9:
        return f"${rev/1e9:.1f}B"
    elif rev >= 1e6:
        return f"${rev/1e6:.0f}M"
    return f"${rev:.0f}"


def fetch_recent_results(days_back: int = 3) -> list[dict]:
    """抓最近幾天已公布的財報結果。"""
    today = date.today()
    from_date = today - timedelta(days=days_back)

    url = (
        f"https://financialmodelingprep.com/stable/earnings-calendar"
        f"?from={from_date}&to={today}&apikey={FMP_API_KEY}"
    )
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"earnings API error: {e}")
        return []

    results = []
    for item in data:
        symbol = item.get("symbol", "")
        eps_actual = item.get("epsActual")
        # 只回傳已有實際數據的紀錄
        if symbol not in WATCHLIST or eps_actual is None:
            continue

        eps_est = item.get("epsEstimated")
        rev_actual = item.get("revenueActual")
        rev_est = item.get("revenueEstimated")

        results.append({
            "symbol": symbol,
            "name": COMPANY_NAMES.get(symbol, symbol),
            "date": item.get("date", ""),
            "eps_actual": eps_actual,
            "eps_est": eps_est,
            "eps_result": _beat_miss(eps_actual, eps_est),
            "rev_actual": _fmt_revenue(rev_actual),
            "rev_est": _fmt_revenue(rev_est),
            "rev_result": _beat_miss(rev_actual, rev_est),
        })

    results.sort(key=lambda x: x["date"], reverse=True)
    return results
