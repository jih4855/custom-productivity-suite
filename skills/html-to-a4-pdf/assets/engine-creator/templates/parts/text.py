"""범용 텍스트 블록 파츠 — 조항, 본문, 설명 등 자유 텍스트"""
from html import escape


def html_text(value) -> str:
    return escape(str(value or ""), quote=False)


def css(data: dict) -> str:
    return """
        /* ── Text Block ── */
        .text-block { margin-bottom: 0; }
        .text-block + .text-block { margin-top: 18px; }
        .text-block h3 {
            font-size: 15px; font-weight: 700; color: var(--text-dark);
            margin-bottom: 7px;
        }
        .text-block p {
            font-size: 14px; line-height: 1.8; color: #374151;
        }
        .text-block p + p { margin-top: 6px; }"""


def render(data: dict, key: str = None) -> str:
    """
    JSON 예시:
        "intro": { "type": "text", "title": "서론", "content": "본문...\\n\\n두 번째 단락" }
    """
    block = data.get(key, {}) if key else {}
    title = block.get("title", "")
    content = block.get("content", "")

    title_html = f'        <h3>{html_text(title)}</h3>\n' if title else ""
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    if paragraphs:
        parts_html = [f"        <p>{html_text(p)}</p>" for p in paragraphs]
        body_html = "\n        <br>\n".join(parts_html)
    else:
        body_html = "        <p></p>"
    return f"""
    <div class="text-block">
{title_html}{body_html}
    </div>"""
