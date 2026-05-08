# engine-creator

반복 생성 문서를 위한 새 엔진 뼈대를 만드는 스캐폴더입니다.
생성 결과물은 현재 레포 루트 바로 아래에 만들어집니다.

## 사용법

```bash
python3 assets/engine-creator/scaffold.py 계약서
python3 assets/engine-creator/scaffold.py proposal --force
```

- 첫 번째 인자: 생성할 폴더명
- `--force`: 같은 이름의 폴더가 있으면 지우고 다시 생성

## 생성 결과

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

## 생성 후 기본 흐름

```bash
# 1. 엔진 생성
python3 assets/engine-creator/scaffold.py 계약서

# 2. 샘플 데이터 수정
$EDITOR 계약서/data.json

# 3. HTML 생성
python3 계약서/render.py 계약서/data.json

# 4. PDF까지 생성
python3 계약서/render.py 계약서/data.json --pdf
```

## 템플릿 구조

- `render.py`: 페이지 분배, CSS 조립, PDF 변환 연동
- `data.json`: 샘플 문서 데이터
- `parts/text.py`: 범용 제목+본문 블록
- `parts/table.py`: 범용 표
- `parts/signature.py`: 서명란
- `parts/base.py`: 문서 CSS와 `a4-base.css` 로드

## CSS 책임 분리

- 상위 `assets/a4-base.css`는 A4 셸입니다.
  `.page` 크기, 페이지 브레이크, print/screen 공통 셸을 담당합니다.
- `parts/base.py`는 문서 스타일 레이어입니다.
  폰트, 색상, 섹션/카드 스타일, 문서별 `.page` padding만 다룹니다.
- `parts/base.py`에서 다시 정의하지 말아야 하는 것:
  `.page`의 `width`/`height`, `page-break-*`, `break-*`, `@page`
- 문서별 여백을 바꾸려면 `style.page-margin` 또는 `.page { padding: ... }`만 사용합니다.

## 커스터마이징 규칙

### 새 파츠 추가

1. `parts/my_part.py` 생성
2. `css(data)`와 `render(data, key=None)` 구현
3. `parts/__init__.py`에 import 및 `PARTS` 등록
4. `data.json`에서 `type` 또는 섹션명으로 호출

### 섹션 타입 재사용

```json
"intro": {
  "type": "text",
  "title": "서론",
  "content": "본문"
}
```

### 여러 섹션 묶기

```json
"body": {
  "wrap": ["intro", "overview"],
  "grow": true
}
```

`grow: true`를 쓰면 마지막 섹션 또는 래퍼가 페이지의 남은 공간을 채웁니다.

### 페이지 나누기

```json
"sections": ["intro", "overview", "---", "sign"]
```

## 주의할 점

- 이 스캐폴더는 제네릭 템플릿만 제공합니다.
- 특정 도메인 전용 엔진은 생성 후 각자 파츠를 확장해야 합니다.
- 레이아웃 조정은 여백을 줄이는 방식보다 콘텐츠와 페이지 분배를 조정하는 쪽을 우선합니다.
