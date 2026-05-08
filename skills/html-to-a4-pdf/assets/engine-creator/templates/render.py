#!/usr/bin/env python3
"""
{DOMAIN} 문서 생성 엔진 — JSON → HTML → PDF

메인 엔진: 페이지 분배, grow 처리, CSS 조립
각 섹션의 HTML/CSS는 parts/ 폴더에서 담당.

사용법:
    python render.py data.json              # HTML 생성
    python render.py data.json --pdf        # HTML + PDF 변환
    python render.py data.json --open       # HTML 생성 후 열기
    python render.py data.json -o 출력.html # 출력 파일명 지정
"""

import json
import argparse
import subprocess  # PDF 미리보기(open 명령) 용 — PDF 생성은 상위 convert.py가 담당
import webbrowser
import os
import sys
from html import escape

from parts import PARTS, collect_css
from parts.base import base_css


def find_upwards(start_dir: str, filename: str) -> str:
    """Find a shared asset by walking up from generated engine folders."""
    current = os.path.abspath(start_dir)
    while True:
        candidate = os.path.join(current, filename)
        if os.path.exists(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            return ""
        current = parent


def html_text(value) -> str:
    """Escape JSON values before inserting them into HTML text nodes."""
    return escape(str(value or ""), quote=False)


# ────────────────────────────────────────
# 범용 엔진 — 도메인 무관
# ────────────────────────────────────────

def build_style(data: dict, used_parts: list) -> str:
    """공통 CSS + 사용된 파츠의 CSS만 합쳐서 <style> 블록 생성"""
    return f"""
    <style>
{base_css(data)}
{collect_css(data, used_parts)}
    </style>"""


def render_section(data: dict, sec: str) -> str:
    """단일 섹션을 렌더링. 섹션명에 따라 적절한 파츠 호출."""
    sec_data = data.get(sec, {})

    # type 지정 섹션: 같은 파츠(text 등)를 여러 번 재사용
    if isinstance(sec_data, dict) and sec_data.get("type"):
        part = PARTS.get(sec_data["type"])
        if not part:
            return ""
        return part.render(data, key=sec)

    # wrap 섹션: 여러 섹션을 하나의 카드 박스로 묶기
    if isinstance(sec_data, dict) and "wrap" in sec_data:
        return render_wrap(data, sec)

    # 일반 파츠 조회 (섹션명 = 파츠명)
    part = PARTS.get(sec)
    if not part:
        return ""
    return part.render(data)


def render_wrap(data: dict, key: str) -> str:
    """여러 섹션을 하나의 카드 박스로 묶어서 렌더링"""
    wrap_data = data.get(key, {})
    child_keys = wrap_data.get("wrap", [])
    inner_html = ""
    for child_key in child_keys:
        inner_html += render_section(data, child_key)
    return f'    <div class="section-wrap">\n{inner_html}\n    </div>'


def render_html(data: dict) -> str:
    """JSON 데이터를 받아 전체 HTML 문자열 생성"""
    sections = data.get("sections", list(PARTS.keys()))

    header_data = data.get("header", {})
    doc_title = html_text(header_data.get("title") or data.get("title", "문서"))

    # 사용된 파츠 이름 수집 (CSS 최적화용)
    used_parts = []
    for sec in sections:
        if sec == "---":
            continue
        sec_data = data.get(sec, {})
        if isinstance(sec_data, dict) and sec_data.get("type"):
            used_parts.append(sec_data["type"])
        elif isinstance(sec_data, dict) and "wrap" in sec_data:
            for child in sec_data["wrap"]:
                child_data = data.get(child, {})
                if isinstance(child_data, dict) and child_data.get("type"):
                    used_parts.append(child_data["type"])
                else:
                    used_parts.append(child)
            used_parts.append(sec)
        else:
            used_parts.append(sec)

    # "---"로 페이지 분리
    pages_html = []
    current = []
    for sec in sections:
        if sec == "---":
            if current:
                pages_html.append("".join(current))
                current = []
            continue

        sec_data = data.get(sec, {})
        chunk = render_section(data, sec)

        # grow: true → 해당 섹션/wrap이 남은 공간 전부 차지
        if isinstance(sec_data, dict) and sec_data.get("grow"):
            chunk = chunk.replace('class="section-wrap"', 'class="section-wrap grow-section"', 1)
            chunk = chunk.replace("    <section>", '    <section class="grow-section">', 1)

        current.append(chunk)

    if current:
        pages_html.append("".join(current))

    page_divs = "\n".join(
        f'<div class="page">\n{page_html}\n</div>' for page_html in pages_html
    )

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{doc_title}</title>
{build_style(data, used_parts)}
</head>
<body>

{page_divs}

</body>
</html>"""


# ────────────────────────────────────────
# 이미지 경로 범용 처리
# ────────────────────────────────────────

def resolve_images(node, base_dir: str):
    """JSON 트리를 재귀적으로 돌며 image/images 키를 절대경로로 변환"""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "image" and isinstance(v, str) and v and not os.path.isabs(v):
                node[k] = os.path.abspath(os.path.join(base_dir, v))
            elif k == "images" and isinstance(v, list):
                node[k] = [
                    os.path.abspath(os.path.join(base_dir, p)) if isinstance(p, str) and not os.path.isabs(p) else p
                    for p in v
                ]
            else:
                resolve_images(v, base_dir)
    elif isinstance(node, list):
        for item in node:
            resolve_images(item, base_dir)


# ────────────────────────────────────────
# CLI
# ────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="{DOMAIN} 엔진 — JSON → HTML → PDF")
    parser.add_argument("input", help="JSON 데이터 파일 경로")
    parser.add_argument("-o", "--output", help="출력 HTML 경로 (기본: 입력파일명.html, 현재 폴더 기준)")
    parser.add_argument("--pdf", action="store_true", help="PDF도 함께 생성")
    parser.add_argument("--open", action="store_true", help="생성 후 열기")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[에러] 파일을 찾을 수 없습니다: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 이미지 경로 변환 (JSON 파일 기준)
    json_dir = os.path.dirname(os.path.abspath(args.input))
    resolve_images(data, json_dir)

    # HTML 생성
    html = render_html(data)

    # 출력 파일명 결정 (기본: JSON 파일과 같은 폴더)
    if args.output:
        out_html = os.path.abspath(args.output)
    else:
        base = os.path.splitext(os.path.basename(args.input))[0]
        out_html = os.path.join(json_dir, base + ".html")

    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[완료] HTML 생성: {out_html}")

    # PDF 변환 — 상위 폴더(html-to-a4-pdf)의 convert.py 재사용
    if args.pdf:
        out_pdf = os.path.splitext(out_html)[0] + ".pdf"
        convert_path = find_upwards(os.path.dirname(os.path.abspath(__file__)), "convert.py")
        if convert_path:
            sys.path.insert(0, os.path.dirname(convert_path))
        try:
            if not convert_path:
                raise ImportError
            from convert import convert_html_to_pdf
            convert_html_to_pdf(out_html, out_pdf)
        except ImportError:
            print("[에러] 상위 폴더의 convert.py를 찾을 수 없습니다. PDF 변환을 건너뜁니다.")
        finally:
            if convert_path:
                sys.path.pop(0)

    if args.open:
        if args.pdf:
            subprocess.run(["open", os.path.abspath(out_pdf)])
            print(f"[열기] PDF: {out_pdf}")
        else:
            webbrowser.open(f"file://{os.path.abspath(out_html)}")
            print("[열기] HTML 미리보기 중...")


if __name__ == "__main__":
    main()
