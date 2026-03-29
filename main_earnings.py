# main_earnings.py — 每日推送已公布的財報結果
from fetchers.earnings import fetch_recent_results
from publishers.line import push_blocks
from storage.db import init_db, already_pushed, mark_pushed


def main():
    init_db()
    print("抓取近期財報結果...")
    results = fetch_recent_results(days_back=2)

    new_results = [r for r in results if not already_pushed(r["symbol"], r["date"])]
    print(f"新財報：{len(new_results)} 筆")

    if not new_results:
        print("無新財報")
        return

    blocks = []
    for r in new_results:
        eps_line = f"EPS：${r['eps_actual']:.2f}"
        if r['eps_est']:
            eps_line += f"（預估 ${r['eps_est']:.2f}）{r['eps_result']}"
        rev_line = f"營收：{r['rev_actual']}"
        if r['rev_est'] != "N/A":
            rev_line += f"（預估 {r['rev_est']}）{r['rev_result']}"
        block = f"🏢 {r['symbol']} {r['name']}  [{r['date']}]\n{eps_line}\n{rev_line}"
        blocks.append(block)

    push_blocks("💰 財報速報", blocks)

    for r in new_results:
        mark_pushed(r["symbol"], r["date"])
    print(f"已推送 {len(new_results)} 筆並記錄")


if __name__ == "__main__":
    main()
