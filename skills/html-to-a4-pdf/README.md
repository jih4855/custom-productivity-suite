# html-to-a4-pdf

Chrome headless 기반으로 HTML 문서를 A4 PDF로 안정적으로 변환하는 도구 모음입니다.
반복 생성 문서는 `assets/engine-creator/`로 전용 엔진을 스캐폴딩해 JSON 기반으로 관리할 수 있습니다.

이 스킬은 이 레포의 핵심 포트폴리오 항목입니다. HTML/CSS로 세밀한 A4 레이아웃을 만들고, Python CLI로 PDF 변환까지 자동화하여 제안서, 계약서, 보고서, 이력서형 문서를 반복 생성할 수 있는 구조를 보여줍니다.

## 포함 내용

- `assets/convert.py`: 단일 HTML 파일을 PDF로 변환하는 범용 CLI
- `assets/a4-base.css`: 하드 페이지 A4 레이아웃 공통 CSS
- `assets/engine-creator/`: 새 문서 엔진 스캐폴더와 기본 파츠 템플릿
- `SKILL.md`: 에이전트/사용자용 상세 운영 가이드

이 레포는 **공통 코어와 제네릭 템플릿만** 포함합니다.
도메인별 레퍼런스 엔진이나 예제 산출물은 넣지 않아 공개 상태를 최소한으로 유지합니다.

## 요구 사항

- Python 3.9+
- Chrome 또는 Chromium 계열 브라우저
- macOS 기본 경로는 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- 다른 경로를 쓰면 `CHROME_BIN` 환경변수로 지정

```bash
export CHROME_BIN="/path/to/chrome"
```

현재 Python 표준 라이브러리만 사용하므로 필수 패키지 의존성은 없습니다.

## 빠른 사용

### 1. 단발성 문서

```bash
python3 assets/convert.py my_document.html -o my_document.pdf
```

HTML에서 공통 여백 규칙을 쓰려면 다음처럼 CSS를 연결합니다.

```html
<link rel="stylesheet" href="assets/a4-base.css">
```

문서별 폰트/색상/섹션 스타일은 별도 `<style>` 블록이나 내부 CSS에 둡니다.

### 2. 반복 생성 문서

```bash
# 1. 엔진 생성
python3 assets/engine-creator/scaffold.py 계약서

# 2. 샘플 데이터 수정
$EDITOR 계약서/data.json

# 3. HTML + PDF 생성
python3 계약서/render.py 계약서/data.json --pdf
```

생성된 엔진에는 다음 파일이 들어 있습니다.

```text
계약서/
├── data.json
├── render.py
└── parts/
    ├── __init__.py
    ├── base.py
    ├── signature.py
    ├── table.py
    └── text.py
```

## 폴더 구조

```text
html-to-a4-pdf/
├── README.md
├── SKILL.md
└── assets/
    ├── a4-base.css
    ├── convert.py
    ├── requirements.txt
    └── engine-creator/
        ├── SKILL.md
        ├── scaffold.py
        └── templates/
```

## 제작 원칙

- PDF는 Chrome headless로만 변환
- 페이지는 연속 스크롤이 아니라 **하드 페이지 A4** 기준으로 설계
- 여백은 `@page margin`이 아니라 `.page` padding으로 제어
- 반복 문서는 HTML 직접 복붙보다 **JSON + 파츠** 구조를 우선

## 공개 레포 위생

- 실제 이력서, 고객 문서, 계약서, 견적서, 생성 PDF는 포함하지 않습니다.
- `assets/engine-creator/templates/data.json`은 동작 설명용 제네릭 샘플입니다.
- 로컬 `data.json`, 생성 PDF, `.env`, 캐시, OS 메타 파일은 루트 `.gitignore`에서 제외합니다.

## CSS 역할 분리

- `assets/a4-base.css`는 문서 공통 A4 셸입니다.
  `.page` 크기, 기본 padding, 페이지 브레이크, print/screen 셸, 절단 방지 유틸리티만 담당합니다.
- 문서 내부 CSS는 타이포그래피, 색상, 섹션/카드 스타일을 담당합니다.
  엔진 스캐폴더 기준으로는 `parts/base.py`가 이 역할입니다.
- 문서 내부 CSS에서 허용하는 A4 관련 오버라이드는 `.page { padding: ... }` 정도로 제한합니다.
- 문서 내부 CSS에서 다시 정의하지 말아야 하는 것:
  `.page`의 `width`/`height`, `page-break-*`, `break-*`, `@page`

자세한 운영 가이드는 [SKILL.md](SKILL.md), 엔진 생성 세부 규칙은 [assets/engine-creator/SKILL.md](assets/engine-creator/SKILL.md) 참고.
