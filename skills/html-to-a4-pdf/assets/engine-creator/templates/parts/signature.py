"""서명란 파츠 — 계약서 하단 서명 영역"""
from html import escape


def html_text(value) -> str:
    return escape(str(value or ""), quote=False)


def css(data: dict) -> str:
    return """
        /* ── Signature ── */
        .signature-area { margin-top: auto; padding-top: 20px; }
        .signature-row {
            display: flex; justify-content: space-between; gap: 40px;
        }
        .signature-block { flex: 1; }
        .signature-block h4 {
            font-size: 14px; font-weight: 700; margin-bottom: 12px;
            padding-bottom: 4px; border-bottom: 1px solid var(--gray-border);
        }
        .signature-line {
            display: flex; justify-content: space-between; align-items: baseline;
            margin-bottom: 8px; font-size: 13px;
        }
        .signature-line .label { font-weight: 600; color: #374151; }
        .signature-line .value {
            flex: 1; margin-left: 10px;
            border-bottom: 1px solid var(--gray-border);
            min-height: 20px;
        }"""


def render(data: dict, key: str = None) -> str:
    """
    JSON 예시:
        "sign": { "type": "signature", "parties": [
            { "role": "갑", "fields": ["회사명","대표자","서명"] },
            { "role": "을", "fields": ["성명","주소","서명"] }
        ]}
    """
    block = data.get(key, {}) if key else {}
    parties = block.get("parties", [])

    html = '    <div class="signature-area">\n        <div class="signature-row">\n'
    for party in parties:
        role = party.get("role", "")
        fields = party.get("fields", [])
        html += f'            <div class="signature-block">\n'
        html += f'                <h4>{html_text(role)}</h4>\n'
        for field in fields:
            html += f'                <div class="signature-line"><span class="label">{html_text(field)}</span><span class="value"></span></div>\n'
        html += f'            </div>\n'
    html += '        </div>\n    </div>'
    return html
