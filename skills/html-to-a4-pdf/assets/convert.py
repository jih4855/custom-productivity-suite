#!/usr/bin/env python3
"""HTML 문서를 Chrome headless로 A4 PDF로 변환한다."""
import argparse
import os
import subprocess
import sys


class PdfConversionError(RuntimeError):
    """PDF 변환 실패 시 호출자에게 원인을 전달한다."""


def convert_html_to_pdf(input_html, output_pdf=None):
    """입력 HTML을 PDF로 변환하고 출력 PDF 절대경로를 반환한다."""
    if not os.path.exists(input_html):
        raise PdfConversionError(f"입력 파일을 찾을 수 없습니다: {input_html}")

    if not output_pdf:
        output_pdf = os.path.splitext(input_html)[0] + ".pdf"

    chrome = os.environ.get(
        "CHROME_BIN",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    )
    if not os.path.exists(chrome):
        raise PdfConversionError(
            "Chrome을 찾을 수 없습니다. "
            f"경로: {chrome}. "
            "필요하면 CHROME_BIN 환경변수로 실행 파일 경로를 지정하세요."
        )

    abs_input = os.path.abspath(input_html)
    abs_output = os.path.abspath(output_pdf)
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--print-to-pdf={abs_output}",
        "--no-margins",
        "--virtual-time-budget=10000",
        f"file://{abs_input}",
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise PdfConversionError("PDF 변환 실패: Chrome 렌더링 60초 초과") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace")
        raise PdfConversionError(f"PDF 변환 실패:\n{stderr}") from exc

    print(f"[완료] PDF 생성: {abs_output}")
    return abs_output

def main():
    parser = argparse.ArgumentParser(description="HTML 문서를 A4 규격 PDF로 변환 (Chrome Headless)")
    parser.add_argument("input", help="입력 HTML 파일 경로")
    parser.add_argument("-o", "--output", help="출력 PDF 파일 경로 (기본값: 원본파일명.pdf)")

    args = parser.parse_args()
    try:
        convert_html_to_pdf(args.input, args.output)
    except PdfConversionError as exc:
        print(f"[에러] {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
