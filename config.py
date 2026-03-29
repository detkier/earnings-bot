import os
from dotenv import load_dotenv

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# 重點觀察名單：科技、半導體、金融、消費
WATCHLIST = {
    "AAPL", "MSFT", "GOOGL", "GOOG", "META", "AMZN", "NVDA", "TSLA",
    "AMD", "INTC", "AVGO", "QCOM", "MU", "ORCL", "CRM", "NFLX", "UBER",
    "TSM", "ASML", "AMAT", "LRCX", "TXN", "ADBE", "NOW", "PANW",
    "JPM", "BAC", "GS", "MS", "V", "MA", "WFC", "C",
    "UNH", "LLY", "WMT", "DIS", "F", "BABA", "FDX", "SBUX",
    "GILD", "PFE", "MRNA", "TMO", "COST",
}

COMPANY_NAMES = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", "GOOG": "Google",
    "META": "Meta", "AMZN": "Amazon", "NVDA": "NVIDIA", "TSLA": "Tesla",
    "AMD": "AMD", "INTC": "Intel", "AVGO": "Broadcom", "QCOM": "Qualcomm",
    "MU": "Micron", "TSM": "TSMC", "ORCL": "Oracle", "CRM": "Salesforce",
    "NFLX": "Netflix", "UBER": "Uber", "ASML": "ASML", "AMAT": "Applied Materials",
    "LRCX": "Lam Research", "TXN": "TI", "ADBE": "Adobe", "NOW": "ServiceNow",
    "PANW": "Palo Alto", "JPM": "JPMorgan", "BAC": "Bank of America",
    "GS": "Goldman Sachs", "MS": "Morgan Stanley", "V": "Visa", "MA": "Mastercard",
    "WFC": "Wells Fargo", "C": "Citigroup", "UNH": "UnitedHealth", "LLY": "Eli Lilly",
    "WMT": "Walmart", "DIS": "Disney", "F": "Ford", "BABA": "Alibaba",
    "FDX": "FedEx", "SBUX": "Starbucks", "GILD": "Gilead", "PFE": "Pfizer",
    "MRNA": "Moderna", "TMO": "Thermo Fisher", "COST": "Costco",
    "CCL": "Carnival", "ETSY": "Etsy", "MGM": "MGM",
}
