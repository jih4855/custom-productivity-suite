"""Build a vanilla-presentation HTML deck from a JSON spec."""

import json
import os
import argparse
from html import escape
from urllib.parse import urlparse


def text(value) -> str:
    """Escape JSON values before inserting them into HTML text nodes."""
    return escape(str(value or ""), quote=False)


def attr(value) -> str:
    """Escape JSON values before inserting them into HTML attributes."""
    return escape(str(value or ""), quote=True)


def safe_url(value, allowed_schemes=("http", "https", "mailto", "")) -> str:
    """Allow only browser-safe URL schemes in generated links/media."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme and parsed.scheme not in allowed_schemes:
        return ""
    if parsed.scheme == "" and raw.startswith("//"):
        return ""
    return attr(raw)


def safe_media_src(value) -> str:
    """Allow http(s), root-relative, and local relative media paths."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return ""
    if raw.startswith("//"):
        return ""
    return attr(raw)


# ─────────────────────────────────────────
# 컴포넌트 렌더러
# ─────────────────────────────────────────

def render_component(comp):
    """SKILL.md §3.3 컴포넌트 카탈로그에 정의된 type → HTML 변환.
    클래스명은 테마 CSS와 1:1 매핑되며 접두어(ppt-) 없이 사용한다.
    """
    ctype = comp.get("type")

    # ── 내용/데이터 ─────────────────────────────
    if ctype == "cards":
        html = '<div class="cards">'
        for item in comp.get("items", []):
            html += f'''
            <div class="card">
              <strong>{text(item.get('title'))}</strong>
              <span>{text(item.get('desc'))}</span>
            </div>'''
        html += '</div>'
        return html

    elif ctype == "flow":
        html = '<div class="flow">'
        for item in comp.get("items", []):
            html += f'''
            <div class="node">
              <h3>{text(item.get('title'))}</h3>
              <p>{text(item.get('desc'))}</p>
            </div>'''
        html += '</div>'
        return html

    elif ctype == "contract":
        html = '<div class="contract">'
        for item in comp.get("items", []):
            html += f'''
            <div class="node">
              <h3>{text(item.get('title'))}</h3>
              <p>{text(item.get('desc'))}</p>
            </div>'''
        html += '</div>'
        return html

    elif ctype == "split":
        html = '<div class="split">'
        for item in comp.get("items", []):
            html += f'''
            <div class="path">
              <strong>{text(item.get('title'))}</strong>
              <p>{text(item.get('desc'))}</p>
            </div>'''
        html += '</div>'
        return html

    elif ctype == "table":
        html = '<table><thead><tr>'
        for h in comp.get("headers", []):
            html += f'<th>{text(h)}</th>'
        html += '</tr></thead><tbody>'
        for row in comp.get("rows", []):
            html += '<tr>' + ''.join(f'<td>{text(cell)}</td>' for cell in row) + '</tr>'
        html += '</tbody></table>'
        return html

    elif ctype == "checklist":
        html = '<ul class="checklist">'
        for item in comp.get("items", []):
            html += f'<li class="check-item">{text(item.get("text"))}</li>'
        html += '</ul>'
        return html

    elif ctype == "timeline":
        html = '<div class="timeline">'
        for item in comp.get("items", []):
            html += f'''
            <div class="timeline-item">
              <strong>{text(item.get('date'))}</strong>
              <span>{text(item.get('desc'))}</span>
            </div>'''
        html += '</div>'
        return html

    elif ctype == "image":
        src = safe_media_src(comp.get("src"))
        alt = attr(comp.get("alt"))
        if not src:
            return '<div class="image-frame" aria-label="Image placeholder"></div>'
        return f'''<div class="image-frame">
          <img src="{src}" alt="{alt}">
        </div>'''

    elif ctype == "video":
        autoplay = "autoplay muted playsinline" if comp.get("autoplay", False) else ""
        loop = "loop" if comp.get("loop", False) else ""
        controls = "controls" if comp.get("controls", True) else ""
        src = safe_media_src(comp.get("src"))
        if not src:
            return '<div class="video-frame" aria-label="Video placeholder"></div>'
        return f'''<div class="video-frame">
          <video src="{src}" {autoplay} {loop} {controls}></video>
        </div>'''

    # ── 구조/요약 ─────────────────────────────
    elif ctype == "toc":
        html = '<ul class="toc">'
        for item in comp.get("items", []):
            html += f'''<li class="toc-item">
              <span>{text(item.get('title'))}</span>
              <span>{text(item.get('page'))}</span>
            </li>'''
        html += '</ul>'
        return html

    elif ctype == "summary":
        return f'<div class="summary"><p>{text(comp.get("text"))}</p></div>'

    # ── 보조/강조 ─────────────────────────────
    elif ctype == "keyMessage":
        return f'<div class="key-message">{text(comp.get("message"))}</div>'

    elif ctype == "banner":
        style = comp.get("style", "")
        style_cls = f' {attr(style)}' if style else ""
        return f'<div class="banner{style_cls}">{text(comp.get("text"))}</div>'

    elif ctype == "source":
        return f'<div class="source">{text(comp.get("text"))}</div>'

    elif ctype == "cta":
        href = safe_url(comp.get("href", "#")) or "#"
        return f'<a class="cta" href="{href}">{text(comp.get("text"))}</a>'

    elif ctype == "map":
        html = '<div class="map">'
        for item in comp.get("items", []):
            html += f'''
            <div class="box">
              <strong>{text(item.get('title'))}</strong>
              <span>{text(item.get('desc'))}</span>
            </div>'''
        html += '</div>'
        return html

    return f"<!-- Unsupported component type: {text(ctype)} -->"

# ─────────────────────────────────────────
# 슬라이드 렌더러
# ─────────────────────────────────────────

def render_slide(slide, index, total, layout):
    stepW = layout.get("stepW", 1320)
    x = index * stepW
    y = 0

    stype = slide.get("type")
    sid   = attr(slide.get("id", f"s{index+1}"))

    # ── 슬라이드 래퍼 ──────────────────────────────
    html = f'<div id="{sid}" class="step" data-x="{x}" data-y="{y}" style="--x:{x}px; --y:{y}px;">'

    # ── 특수 타입: 풀스크린 중앙 정렬 ──────────────
    if stype == "cover":
        html += f'''
        <div style="display:flex; flex-direction:column; justify-content:center; align-items:flex-start; height:100%;
                    padding: var(--slide-pad-y) var(--slide-pad-x); box-sizing:border-box; max-width:var(--stage-w); margin:auto;">
          <p style="font-size:14px; font-weight:800; letter-spacing:.08em; text-transform:uppercase;
                    color:var(--muted); margin:0 0 clamp(16px,3vh,28px);">{text(slide.get('kicker', 'PRESENTATION'))}</p>
          <h1 style="margin:0 0 clamp(12px,2vh,20px);">{text(slide.get('title'))}</h1>
          <p class="lead" style="margin:0 0 clamp(20px,4vh,40px);">{text(slide.get('subtitle'))}</p>
          <p style="font-size:15px; color:var(--muted); border-top:1px solid var(--line);
                    padding-top:16px; width:100%; margin:0;">{text(slide.get('presenter'))}</p>
        </div>'''

    elif stype == "sectionDivider":
        html += f'''
        <div style="display:flex; flex-direction:column; justify-content:center; align-items:center;
                    text-align:center; height:100%; background:var(--bg-sub);">
          <p style="font-size:14px; font-weight:800; letter-spacing:.08em; text-transform:uppercase;
                    color:var(--muted); margin:0 0 16px;">{text(slide.get('chapter'))}</p>
          <h2 style="font-size:clamp(40px,4vw,56px); margin:0;">{text(slide.get('title'))}</h2>
        </div>'''

    elif stype == "qna":
        html += f'''
        <div style="display:flex; flex-direction:column; justify-content:center; align-items:center;
                    text-align:center; height:100%;">
          <h1 style="font-size:clamp(72px,10vw,120px); margin:0 0 16px;">{text(slide.get('title', 'Q&A'))}</h1>
          <p style="font-size:clamp(20px,2vw,28px); color:var(--muted); margin:0;">{text(slide.get('subtitle'))}</p>
        </div>'''

    # ── 일반 타입: .stage 5층 그리드 ───────────────
    else:
        kicker_text  = text(slide.get("kicker"))
        title_tag    = "h2"
        title_text   = text(slide.get("title"))
        lead_text    = text(slide.get("lead"))
        components   = slide.get("components", [])
        if len(components) > 2:
            raise ValueError(
                f"slide {sid} has {len(components)} components; Max 2 Rule allows at most 2"
            )

        # kicker: 섹션명(왼쪽) + 페이지번호(오른쪽) — 고정 row 1
        kicker_html = f'''<div class="kicker">
          <span>{kicker_text}</span>
          <span>{index + 1} / {total}</span>
        </div>'''

        # title — 고정 row 2
        title_html = f'<{title_tag}>{title_text}</{title_tag}>'

        # lead — 고정 row 3 (없으면 빈 div로 행 유지)
        lead_html = f'<p class="lead">{lead_text}</p>' if lead_text else '<div class="lead" style="display:none;"></div>'

        # 컴포넌트를 stage 직계 자식으로 직접 렌더 (wrapper 제거)
        # → base.css의 ".stage > :is(.cards, .flow, ...)" stretch 셀렉터가 그대로 작동
        comps_html = "".join(render_component(c) for c in components)

        html += f'''
        <div class="stage">
          {kicker_html}
          {title_html}
          {lead_html}
          {comps_html}
        </div>'''

    html += '</div>'  # .step
    return html


# ─────────────────────────────────────────
# 빌더 메인
# ─────────────────────────────────────────

def build(spec_path: str, theme: str, out_path: str, layout_override: dict):
    # build.py 자신의 위치를 기준으로 스킬 폴더 경로 자동 계산
    skill_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. JSON 로드
    with open(spec_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides = data.get("slides", [])

    # 2. 레이아웃: PPT처럼 좌우로만 이동한다.
    layout = data.get("layout", {"stepW": 1320})
    if "grid" in data:
        layout["stepW"] = data["grid"].get("stepW", layout["stepW"])
    layout.update({k: v for k, v in layout_override.items() if v is not None})

    # 3. 슬라이드 렌더링
    slides_html = "".join(render_slide(s, i, len(slides), layout) for i, s in enumerate(slides))

    # 4. 외부 에셋 복사 및 경로 설정
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    
    base_css_src  = os.path.join(skill_dir, "css", "base.css")
    engine_js_src = os.path.join(skill_dir, "js", "engine.js")
    
    if theme.endswith(".css") and os.path.exists(theme):
        theme_css_src = theme
    else:
        theme_css_src = os.path.join(skill_dir, "templates", f"{theme}.css")

    # 결과물 폴더로 파일 복사
    import shutil
    shutil.copy2(base_css_src, os.path.join(out_dir, "base.css"))
    shutil.copy2(theme_css_src, os.path.join(out_dir, "theme.css"))
    shutil.copy2(engine_js_src, os.path.join(out_dir, "engine.js"))

    # 5. 최종 HTML 조립 (외부 파일 링크 방식)
    final_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{text(data.get("deck", "Presentation"))}</title>
    <link rel="stylesheet" href="base.css">
    <link rel="stylesheet" href="theme.css">
</head>
<body>
    <div id="presentation">
        {slides_html}
    </div>
    <script src="engine.js"></script>
</body>
</html>
"""

    # 6. 파일 저장
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[완료] {out_path} 및 외부 에셋(CSS, JS) 생성 완료 (테마: {theme}, 슬라이드: {len(slides)}장)")


# ─────────────────────────────────────────
# CLI 진입점
# ─────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="spec.json → index.html PPT 자동 조립기",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python3 build.py                                  # 기본 실행
  python3 build.py
  python3 build.py -s spec.json -o result.html
  python3 build.py --stepW 1440
        """
    )

    parser.add_argument(
        "-s", "--spec",
        default="spec.json",
        help="JSON 스펙 파일 경로 (기본: spec.json)"
    )
    parser.add_argument(
        "-t", "--theme",
        default="minimal-tech-hero",
        help="templates/ 폴더 안 테마 파일명 — 확장자(.css) 제외 (기본: minimal-tech-hero)"
    )
    parser.add_argument(
        "-o", "--out",
        default="index.html",
        help="출력 HTML 파일명 (기본: index.html)"
    )
    parser.add_argument(
        "--stepW",
        type=int,
        default=None,
        help="슬라이드 가로 간격(px) — JSON의 layout.stepW 를 덮어씀"
    )

    args = parser.parse_args()

    build(
        spec_path=args.spec,
        theme=args.theme,
        out_path=args.out,
        layout_override={"stepW": args.stepW},
    )
