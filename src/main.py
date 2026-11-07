
import os
import json
from pathlib import Path

from google import genai
from google.genai import types

def main():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("找不到 GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    news = """
    新聞標題：人工智慧在教育領域的應用
    新聞內容：越來越多學校使用人工智慧協助教學，
    包括個人化學習、智慧批改與課程規劃。
    """

    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "category": {"type": "string"}
        },
        "required": ["title", "summary", "category"]
    }

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="請將以下新聞整理成繁體中文摘要：" + news,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=schema
        )
    )

    result = json.loads(response.text)

    Path("docs").mkdir(exist_ok=True)
    Path("docs/news.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("AI 新聞摘要產生成功！")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
