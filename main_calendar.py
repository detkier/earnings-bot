# main_calendar.py — 月底預覽下個月財報行事曆
from datetime import date
from calendar import monthrange
from fetchers.calendar import fetch_next_month_calendar
from publishers.line import push_blocks


def main():
    print("抓取下個月財報行事曆...")
    entries = fetch_next_month_calendar()

    if not entries:
        print("沒有找到重點公司財報")
        return

    today = date.today()
    if today.month == 12:
        year, month = today.year + 1, 1
    else:
        year, month = today.year, today.month + 1
    month_str = f"{year}/{month:02d}"

    print(f"找到 {len(entries)} 筆財報")
    blocks = []
    for e in entries:
        eps = f"EPS 預估：${e['eps_est']:.2f}" if e['eps_est'] else ""
        rev = ""
        if e['rev_est']:
            r = e['rev_est']
            if r >= 1e12:
                rev = f"營收預估：${r/1e12:.1f}T"
            elif r >= 1e9:
                rev = f"營收預估：${r/1e9:.1f}B"
        detail = "  ".join(filter(None, [eps, rev]))
        line = f"📅 {e['date']}  {e['symbol']} {e['name']}"
        if detail:
            line += f"\n   {detail}"
        blocks.append(line)

    push_blocks(f"📊 {month_str} 財報行事曆", blocks)
    print(f"已推送 {len(entries)} 筆")


if __name__ == "__main__":
    main()
