---
name: html-to-a4-pdf
description: HTML 문서를 하드 페이지 A4 기준 PDF로 변환하고, 반복 문서용 JSON+parts 엔진을 스캐폴딩하는 공개용 스킬입니다.
---

# HTML → A4 PDF 변환 스킬

HTML 문서를 Chrome headless로 A4 PDF로 변환하는 공통 스킬입니다.
이 레포는 코어 변환기(`assets/convert.py`)와 반복 문서용 스캐폴더(`assets/engine-creator/`)를 제공합니다.

## 전제 조건

- Python 3.9+
- Chrome 또는 Chromium 계열 브라우저
- macOS 기본 경로:
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- 다른 경로를 쓰면 `CHROME_BIN` 환경변수 지정

```bash
export CHROME_BIN="/path/to/chrome"
```

현재 Python 표준 라이브러리만 사용하므로 필수 패키지 설치는 없습니다.

## 현재 레포에 들어 있는 것

```text
html-to-a4-pdf/
├── assets/
│   ├── convert.py
│   ├── a4-base.css
│   ├── engine-creator/
│   │   ├── scaffold.py
│   │   ├── SKILL.md
│   │   └── templates/
│   └── requirements.txt
└── SKILL.md
```

주의:
- 이 공개 레포에는 `resume/`, `examples/` 같은 도메인별 레퍼런스 엔진을 포함하지 않습니다.
- 대신 `assets/engine-creator/`로 동일한 패턴의 새 엔진을 바로 만들 수 있습니다.

## 기본 작업 분기

### A. 단발성 문서

한 번만 만들 문서라면 HTML 한 파일 + `assets/convert.py`만 사용합니다.

```bash
python3 assets/convert.py input.html -o output.pdf
```

### B. 반복 생성 문서

고객별, 회사별, 월별로 계속 찍어낼 문서라면 엔진을 만듭니다.

```bash
python3 assets/engine-creator/scaffold.py 계약서
python3 계약서/render.py 계약서/data.json --pdf
```

## CSS 책임 분리

- `assets/a4-base.css`:
  A4 물리 셸만 담당합니다.
  `.page` 크기, 기본 여백, 페이지 브레이크, `@media print`, 화면 미리보기 셸, 절단 방지 유틸리티가 여기에 있습니다.
- 문서 내부 CSS:
  폰트, 색상, 텍스트 밀도, 카드/섹션 스타일을 담당합니다.
  단발성 문서면 `<style>` 블록, 스캐폴더 엔진이면 `parts/base.py`가 이 역할입니다.
- 허용하는 오버라이드:
  문서별 `.page` padding
- 다시 선언하지 말 것:
  `.page`의 `width`, `height`, `page-break-*`, `break-*`, `@page`

## A4 레이아웃 원칙

### 1. 하드 페이지 방식 사용

모든 문서는 `.page` 단위로 A4 크기를 고정합니다.

```css
.page {
    width: 210mm;
    height: 297mm;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    page-break-after: always;
}
```

### 2. 여백은 padding으로만 제어

`@page margin`과 `.page padding`을 동시에 쓰지 않습니다.

```css
@media print {
    @page { size: A4; margin: 0; }
}

.page {
    padding: 22mm 20mm 20mm;
}
```

이 padding은 문서별 CSS에서만 오버라이드합니다.
`assets/a4-base.css` 자체를 문서마다 수정하는 방식은 피합니다.

### 3. 페이지 분리는 JSON의 `"---"`로 제어

```json
"sections": ["intro", "body", "---", "signature"]
```

### 4. 남는 공간은 `grow: true`로 채움

```json
"body": {
  "wrap": ["intro", "overview"],
  "grow": true
}
```

## 변환기 사용법

### CLI

```bash
python3 assets/convert.py input.html -o output.pdf
```

### 다른 스크립트에서 import

```python
import os
import sys

sys.path.insert(0, os.path.abspath("/path/to/html-to-a4-pdf/assets"))
from convert import convert_html_to_pdf

convert_html_to_pdf("input.html", "output.pdf")
```

`convert_html_to_pdf()`는 성공 시 PDF 경로를 반환하고, 실패 시 `PdfConversionError`를 발생시킵니다.

## 운영 원칙

- HTML만 만들고 끝내지 말고, 실제 PDF까지 확인
- 내용이 넘치면 여백을 깎지 말고 콘텐츠 분량/페이지 분배를 조정
- 반복 문서는 HTML 직접 수정 대신 JSON과 파츠를 수정
- 샘플 엔진 생성 후 `data.json` 기준 렌더가 실제로 동작하는지 검증
- `assets/a4-base.css`와 문서 내부 CSS의 책임을 섞지 않기

## 관련 문서

- [assets/engine-creator/SKILL.md](assets/engine-creator/SKILL.md): 엔진 생성 가이드
