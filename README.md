# Custom Productivity Suite

공개 가능한 형태로 정리한 생산성 자동화 스킬 모음입니다. 현재는 **HTML 기반 A4/PDF 문서 자동화**와 **Vanilla HTML/CSS/JS 프레젠테이션 제작**이라는 두 가지 워크플로우를 담고 있습니다.

## 개요
기존 오피스 도구에서 반복적으로 손으로 맞추던 레이아웃 작업을 코드와 JSON 스펙으로 재현 가능하게 만드는 것이 목적입니다. 모든 도구는 런타임 외부 라이브러리 의존성을 최소화하고 웹 표준(HTML/CSS/JS)과 Python을 기반으로 작동합니다.

이 레포는 완성 산출물 저장소가 아니라, 문서와 발표 자료를 빠르게 만들기 위한 **재사용 가능한 제작 시스템**입니다. 개인정보, 고객 데이터, 도메인별 산출물은 포함하지 않고 공통 코어와 제네릭 템플릿만 제공합니다.

## 포함된 스킬

### HTML to A4 PDF

`skills/html-to-a4-pdf/`는 HTML 문서를 Chrome headless로 A4 PDF로 변환하는 문서 자동화 스킬입니다.

- A4 고정 페이지 레이아웃을 CSS로 관리
- 단발성 HTML 문서 PDF 변환 지원
- 반복 문서용 JSON + 파츠 기반 엔진 스캐폴딩 지원
- 계약서, 제안서, 보고서, 이력서형 문서 자동화 포트폴리오로 확장 가능

### Vanilla Presentation

`skills/vanilla-presentation/`은 외부 프레젠테이션 라이브러리 없이 HTML/CSS/JS만으로 발표 자료를 만드는 스킬입니다.

- JSON 스펙에서 발표 HTML 생성
- `minimal-tech-hero` 단일 템플릿 기반 슬라이드 레이아웃
- 좌우 방향키만 사용하는 단순 프레젠테이션 엔진
- `index.html`, `base.css`, `theme.css`, `engine.js` 4개 파일 묶음으로 실행 가능한 포터블 발표 자료 생성

## 제작 원칙 (Core Principles)
- **Visual-First**: 정보의 홍수 속에서 핵심 시각 정보(표, 다이어그램, 이미지) 위주의 전달을 지향합니다.
- **Lightweight & Portable**: 외부 프레젠테이션 라이브러리 없이, 생성된 HTML/CSS/JS 파일 묶음을 브라우저에서 바로 열 수 있어야 합니다.
- **One Slide, One Message**: 복잡함을 배제하고 하나의 단위에는 하나의 명확한 메시지만 담습니다.
- **Automated Workflow**: 반복적인 문서 작업은 JSON 스펙 기반의 빌드 시스템을 통해 자동화합니다.
- **B2B Aesthetic**: 비즈니스 환경에 적합한 정갈하고 신뢰감 있는 디자인 시스템을 유지합니다.

## 빠른 시작

```bash
# A4 PDF 변환
python3 skills/html-to-a4-pdf/assets/convert.py input.html -o output.pdf

# 프레젠테이션 빌드
python3 skills/vanilla-presentation/assets/build.py \
  -s skills/vanilla-presentation/assets/examples/minimal-tech-hero-demo/master-spec.json \
  -o preview/index.html
```

상세 도구 목록과 운영 가이드는 [SKILLS.md](SKILLS.md)에서 확인할 수 있습니다.

## 공개 위생

- 이 레포에는 실제 고객 데이터, 개인 연락처, API 키, 인증 파일을 포함하지 않습니다.
- 생성된 PDF, 로컬 `data.json`, `.env`, 캐시, 로그, OS 메타 파일, 임의 CSV/XLSX 데이터는 `.gitignore`로 제외합니다.
- 예제는 도구 동작을 설명하기 위한 제네릭 샘플만 포함합니다.

## 라이선스

MIT License. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
