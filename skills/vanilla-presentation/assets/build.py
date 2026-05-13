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
        raw_src = str(comp.get("src", "")).strip()
        if not raw_src:
            return '<div class="video-frame" aria-label="Video placeholder"></div>'
        # YouTube watch URL / youtu.be 단축 URL → embed URL 자동 변환.
        # Vimeo 일반 URL → player URL 자동 변환. (사용자가 일반 공유 URL 그대로 박아도 동작)
        import re as _re
        m = _re.match(r"https?://(?:www\.|m\.)?youtube\.com/watch\?(?:.*&)?v=([\w-]+)", raw_src)
        if m:
            raw_src = f"https://www.youtube.com/embed/{m.group(1)}"
        m = _re.match(r"https?://youtu\.be/([\w-]+)", raw_src)
        if m:
            raw_src = f"https://www.youtube.com/embed/{m.group(1)}"
        m = _re.match(r"https?://(?:www\.)?vimeo\.com/(\d+)", raw_src)
        if m:
            raw_src = f"https://player.vimeo.com/video/{m.group(1)}"
        safe_src = safe_media_src(raw_src)
        if not safe_src:
            return '<div class="video-frame" aria-label="Video placeholder"></div>'
        # YouTube/Vimeo embed URL은 iframe으로 렌더링한다.
        if "youtube.com/embed" in raw_src or "player.vimeo.com" in raw_src:
            return (
                f'<div class="video-frame"><iframe src="{safe_src}" '
                f'loading="lazy" allowfullscreen '
                f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>'
            )
        # 그 외(mp4 등)는 기존 <video> 태그
        autoplay = "autoplay muted playsinline" if comp.get("autoplay", False) else ""
        loop = "loop" if comp.get("loop", False) else ""
        controls = "controls" if comp.get("controls", True) else ""
        return f'<div class="video-frame"><video src="{safe_src}" {autoplay} {loop} {controls}></video></div>'

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
    stepW = layout.get("stepW", 1280)
    x = index * stepW
    y = 0

    stype = slide.get("type") or "content"
    sid   = attr(slide.get("id", f"s{index+1}"))

    # ── 슬라이드 래퍼 ──────────────────────────────
    # step 자체에 슬라이드 타입 클래스 부여 (.step--cover / .step--sectionDivider / .step--qna / .step--content)
    # → 특수 슬라이드는 .step의 padding을 0으로 덮어 풀스크린 디자인이 가능하도록.
    type_cls = f"step--{attr(stype)}"
    html = f'<div id="{sid}" class="step {type_cls}" data-x="{x}" data-y="{y}">'

    # ── 특수 타입: 풀스크린 중앙 정렬 ──────────────
    # 디자인은 모두 테마 CSS (.cover / .divider / .qna)에서 책임진다.
    # build.py는 의미적 클래스만 출력하고 인라인 스타일은 넣지 않는다.
    if stype == "cover":
        html += f'''
        <div class="cover">
          <p class="cover-kicker">{text(slide.get('kicker', 'PRESENTATION'))}</p>
          <h1>{text(slide.get('title'))}</h1>
          <p class="lead">{text(slide.get('subtitle'))}</p>
          <p class="cover-meta">{text(slide.get('presenter'))}</p>
        </div>'''

    elif stype == "sectionDivider":
        html += f'''
        <div class="divider">
          <p class="chapter">{text(slide.get('chapter'))}</p>
          <h2>{text(slide.get('title'))}</h2>
        </div>'''

    elif stype == "qna":
        html += f'''
        <div class="qna">
          <h1>{text(slide.get('title', 'Q&A'))}</h1>
          <p class="qna-subtitle">{text(slide.get('subtitle'))}</p>
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
        lead_html = f'<p class="lead">{lead_text}</p>' if lead_text else '<p class="lead lead--empty" aria-hidden="true"></p>'

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
    layout = data.get("layout", {"stepW": 1280})
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
        help="assets/templates/ 폴더 안 테마 파일명 — 확장자(.css) 제외 (기본: minimal-tech-hero)"
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
