# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Related Projects

`~/earnings-bot` 與 `~/line-news-bot` 共用同一組 LINE 憑證，推送到同一個 LINE 帳號。

## Commands

```bash
# 本地測試
source .venv/bin/activate
python main_calendar.py   # 下週財報行事曆
python main_earnings.py   # 近期已公布財報結果

# 安裝套件
pip install requests python-dotenv
```

GitHub Actions 自動執行，手動觸發：GitHub → Actions → 財報推送 → Run workflow，可選 `mode=calendar` 或 `mode=earnings`。

## Architecture

```
earnings-bot/
  config.py               # API keys、50 家公司觀察名單與中文名稱對照
  fetchers/calendar.py    # 抓下週財報行事曆（週一到週五）
  fetchers/earnings.py    # 抓近期財報結果，計算 EPS/Revenue beat/miss 百分比
  publishers/line.py      # LINE 推送，4500 字分批
  storage/db.py           # SQLite 防重複推送（已推送的 symbol+date 記錄）
  main_calendar.py        # 每週日：預覽下週哪些重點公司開財報
  main_earnings.py        # 每日：推送已公布的 EPS、Revenue 超預期/低預期
  .github/workflows/earnings.yml
```

**流程（行事曆）：** FMP `/stable/earnings-calendar?from=下週一&to=下週五` → 過濾觀察名單 → 格式化 EPS/Revenue 預估 → LINE push。

**流程（財報結果）：** FMP `/stable/earnings-calendar?from=N天前&to=今天` → 過濾觀察名單且 `epsActual != null` → 計算 beat/miss 百分比 → 查 SQLite 去重 → LINE push → 記錄已推送。

## Schedule（台灣時間）

| 時間 | 觸發 | 執行 |
|------|------|------|
| 每天 09:00 | `cron: "0 1 * * *"` | `main_earnings.py`（推送昨日/今日已公布財報） |
| 每週日 08:00 | `cron: "0 0 * * 0"` | `main_calendar.py`（預覽下週財報行事曆） |

## Environment Variables

`.env`（本地）或 GitHub Secrets（CI）：

| 變數 | 用途 |
|------|------|
| `FMP_API_KEY` | Financial Modeling Prep API key |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Messaging API Bearer Token |
| `LINE_USER_ID` | 推送目標用戶 ID（U 開頭） |

## API

**Financial Modeling Prep** `/stable/earnings-calendar`：免費方案可用，支援 `from` / `to` 日期篩選。回傳欄位：`symbol`, `date`, `epsActual`, `epsEstimated`, `revenueActual`, `revenueEstimated`。`epsActual = null` 表示尚未公布。

## Watchlist

約 50 家重點公司，涵蓋科技（AAPL、MSFT、GOOGL、META、AMZN、NVDA、TSLA、AMD、TSM）、半導體（INTC、AVGO、QCOM、MU、ASML、AMAT）、金融（JPM、BAC、GS、MS、V、MA）等，定義在 `config.py` 的 `WATCHLIST` 與 `COMPANY_NAMES`。
