"""범용 표 파츠 — 계약서 조건표, 보고서 데이터표, 요약표 등"""
from html import escape


def html_text(value) -> str:
    return escape(str(value or ""), quote=False)


def css(data: dict) -> str:
    return """
        /* ── Table ── */
        .doc-table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 13px; }
        .doc-table th {
            background: var(--accent); color: white;
            padding: 7px 10px; text-align: left; font-weight: 600;
        }
        .doc-table td {
            padding: 6px 10px; border-bottom: 1px solid var(--gray-border);
        }
        .doc-table tr:nth-child(even) td { background: #f8f9fa; }"""


def render(data: dict, key: str = None) -> str:
    """
    JSON 예시:
        "cost": { "type": "table", "title": "비용 내역",
                  "headers": ["항목","금액"], "rows": [["개발","500"],["운영","200"]] }
    """
    block = data.get(key, {}) if key else {}
    title = block.get("title", "")
    headers = block.get("headers", [])
    rows = block.get("rows", [])

    html = ""
    if title:
        html += f'    <h3 style="font-size: 15px; font-weight: 700; margin-bottom: 4px;">{html_text(title)}</h3>\n'

    html += '    <table class="doc-table">\n'
    if headers:
        html += "        <tr>" + "".join(f"<th>{html_text(h)}</th>" for h in headers) + "</tr>\n"
    for row in rows:
        html += "        <tr>" + "".join(f"<td>{html_text(c)}</td>" for c in row) + "</tr>\n"
    html += "    </table>"
    return html
