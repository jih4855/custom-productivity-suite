"""
파츠 레지스트리 — 섹션명/타입명 → 파츠 모듈 매핑

{DOMAIN} 엔진의 파츠 레지스트리.
새 파츠 추가 시: 1) 이 파일 위에서 import 2) PARTS에 한 줄 등록
"""

from . import (
    text,
    table,
    signature,
)

PARTS = {
    # ── 범용 파츠 (모든 문서 공통) ──
    "text": text,
    "table": table,
    "signature": signature,

    # ── {DOMAIN} 전용 파츠 등록 영역 ──
    # 예: "my_custom_section": my_custom_section,
}


def collect_css(data: dict, used_names: list = None) -> str:
    """사용된 파츠의 CSS만 수집. None이면 전체."""
    seen = set()
    css_chunks = []
    targets = used_names if used_names else list(PARTS.keys())

    for name in targets:
        if name in seen:
            continue
        seen.add(name)

        part = PARTS.get(name)
        if part and hasattr(part, "css"):
            css_chunks.append(part.css(data))

    return "\n".join(css_chunks)
