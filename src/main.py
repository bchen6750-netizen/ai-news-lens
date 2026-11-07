
import os
import json
from pathlib import Path
from openai import OpenAI

api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("找不到 OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

news = """
標題：人工智慧在教育領域的應用
內容：越來越多學校使用人工智慧協助教學，
包括個人化學習、智慧批改與課程規劃。
"""

print("正在呼叫免費雲端 AI...")

stream = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "system",
            "content": "你是專業新聞編輯，使用繁體中文回答。"
        },
        {
            "role": "user",
            "content": (
                "請根據以下新聞撰寫100字以內的繁體中文摘要，"
                "只輸出摘要文字：\n" + news
            )
        }
    ],
    stream=True,
)

summary = ""

for chunk in stream:
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            summary += content
            print(content, end="", flush=True)

if not summary.strip():
    raise RuntimeError("AI 沒有產生摘要")

result = {
    "title": "人工智慧在教育領域的應用",
    "summary": summary.strip(),
    "model": "openrouter/free"
}

Path("docs").mkdir(exist_ok=True)

Path("docs/news.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nAI 新聞摘要產生成功！")
