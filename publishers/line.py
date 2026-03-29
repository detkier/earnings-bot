import requests
from config import LINE_TOKEN, LINE_USER_ID

MAX_CHARS = 4500


def push_message(text: str) -> bool:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}",
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": text}],
    }
    resp = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=payload,
        timeout=10,
    )
    if resp.status_code == 200:
        print("推送成功")
        return True
    else:
        print(f"推送失敗：{resp.status_code} {resp.text}")
        return False


def push_blocks(header: str, blocks: list[str]) -> None:
    """分批推送，每則不超過 MAX_CHARS。"""
    current = header + "\n\n"
    for block in blocks:
        if len(current) + len(block) + 2 > MAX_CHARS:
            push_message(current.strip())
            current = header + "（續）\n\n" + block + "\n\n"
        else:
            current += block + "\n\n"
    if current.strip():
        push_message(current.strip())
