"""
공통 유틸리티 — a4-base.css(A4 셸) 위에 문서별 스타일을 얹는 레이어

상위 폴더(html-to-a4-pdf)의 a4-base.css를 로드하고
문서 공통 토큰(색상, 폰트, 섹션 스타일 등)을 주입한다.

주의:
- A4 물리 규격(.page width/height, page-break, @page)은 a4-base.css가 담당
- 이 파일에서는 문서 스타일과 .page padding 오버라이드만 정의
"""
import os


def _find_upwards(start_dir: str, filename: str) -> str:
    """Find a shared asset by walking up from generated engine folders."""
    current = os.path.abspath(start_dir)
    while True:
        candidates = [
            os.path.join(current, filename),
            os.path.join(current, "assets", filename),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        parent = os.path.dirname(current)
        if parent == current:
            return ""
        current = parent


def _css(data: dict, section: str, key: str, default: str) -> str:
    """JSON의 섹션별 css 객체에서 값 꺼내기. 없으면 기본값."""
    sec = data.get(section, {})
    if isinstance(sec, dict):
        return sec.get("css", {}).get(key, default)
    return default


def base_css(data: dict) -> str:
    """문서 스타일, 리셋, 토큰 CSS"""
    s = data.get("style", {})

    # 상위 폴더의 a4-base.css 읽기
    css_path = _find_upwards(os.path.dirname(os.path.abspath(__file__)), "a4-base.css")
    a4_css = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            a4_css = f.read()
    else:
        print(f"[경고] 공통 CSS 파일을 찾을 수 없습니다: {css_path}")

    return f"""
{a4_css}

        :root {{
            --bg-white: #FFFFFF;
            --text-dark: {s.get("text-dark", "#1F2937")};
            --accent: {s.get("accent", "#1E3A5F")};
            --accent-light: {s.get("accent-light", "#EFF6FF")};
            --gray-light: #F3F4F6;
            --gray-border: #E5E7EB;
            --green: #059669;
            --green-light: #ECFDF5;
            --orange: #D97706;
            --orange-light: #FFFBEB;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Malgun Gothic', 'Noto Sans KR', sans-serif;
            color: var(--text-dark);
            word-break: keep-all;
            overflow-wrap: break-word;
            font-size: {s.get("font-size-body", "15px")};
            line-height: {s.get("line-height", "1.6")};
        }}

        /* ── 문서별 페이지 여백 오버라이드 ── */
        .page {{
            padding: {s.get("page-margin", "22mm 20mm 20mm")};
        }}

        /* ── 공통 섹션 ── */
        section {{ margin-bottom: 10px; }}
        h2.section-title {{
            font-size: 17px; font-weight: 700; color: var(--text-dark);
            margin-bottom: 8px; display: flex; align-items: center; gap: 6px;
        }}
        h2.section-title::after {{
            content: ''; flex: 1; height: 2px; background: var(--gray-border);
        }}

        /* ── wrap 박스 ── */
        .section-wrap {{
            border: 1.5px solid var(--gray-border);
            border-radius: 6px;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
        }}
        .section-wrap > section {{ margin-bottom: 10px; }}
        .section-wrap > section:last-child {{ margin-bottom: 0; }}

        /* ── grow — 남은 공간 채우기 ── */
        .grow-section {{ flex-grow: 1; }}
        .section-wrap.grow-section {{ flex-grow: 1; }}
        .section-wrap.grow-section > section:last-child {{
            flex-grow: 1; display: flex; flex-direction: column;
        }}"""
