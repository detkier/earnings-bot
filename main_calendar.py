# main_calendar.py — 每週預覽下週財報行事曆
from fetchers.calendar import fetch_next_week_calendar
from publishers.line import push_blocks


def main():
    print("抓取下週財報行事曆...")
    entries, from_date, to_date = fetch_next_week_calendar()

    if not entries:
        print("下週無重點公司財報")
        push_blocks("📊 下週財報行事曆", ["本週無重點公司財報。"])
        return

    week_str = f"{from_date.strftime('%m/%d')}－{to_date.strftime('%m/%d')}"
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

    push_blocks(f"📊 下週財報行事曆 {week_str}", blocks)
    print(f"已推送 {len(entries)} 筆")


if __name__ == "__main__":
    main()
