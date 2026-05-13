# Vanilla Presentation - 테마 CSS 작성 가이드

`assets/templates/`의 CSS 파일은 재사용 가능한 레퍼런스 템플릿이다. 프레임(클래스명·HTML 구조)은 고정하고, 실제 발표의 디자인(색상·폰트·간격·장식)은 결과물 폴더의 `theme.css`에서 사용자 맞춤형으로 작성한다.

> **테마 생성 시 주의사항 (전수 구현 원칙)**
> 새로운 CSS 테마를 생성할 때는 나중에 어떤 컴포넌트를 꺼내 쓰더라도 디자인이 깨지지 않도록 **SKILL.md의 §3.4 컴포넌트별 JSON 키 & CSS 클래스 매핑에 명시된 모든 컴포넌트 스타일을 반드시 포함해야 한다.**
> 일부 컴포넌트만 구현하는 것은 금지되며, 이는 테마의 범용성과 안정성을 위한 강제 사항이다.

## 1. 필수 구현 클래스 (전수 검사 대상)
아래 클래스는 build.py가 출력하는 HTML과 1:1 대응한다. 새 테마에서 **하나라도 누락되면 안 된다.**

```css
/* 기본 구조 */  .step, .kicker, h1, h2, .lead
/* 특수 슬라이드 */  .cover, .cover-kicker, .cover-meta,
                  .divider, .divider .chapter, .divider h2,
                  .qna, .qna h1, .qna-subtitle
/* 내용/데이터 */  .cards .card strong span, .flow .node h3 p,
                  .split .path strong p, table th td,
                  .checklist .check-item, .timeline .timeline-item,
                  .image-frame, .video-frame, .map .box, .toc .toc-item
/* 보조/강조 */  .key-message, .banner .banner.info .banner.warn,
                .source, .summary
```

## 2. 여백(Spacing) 및 비율 시스템의 통일성
- **하드코딩 금지**: `gap: 32px`, `padding: 16px` 처럼 숫자를 직접 적지 않는다.
- **전역 변수 활용**: `base.css`에 정의된 표준 간격 토큰(`--gap-xs`, `--gap-sm`, `--gap-md`, `--gap-lg`, `--gap-xl`)을 테마 CSS 전반에 일관되게 적용하여 전체 템플릿의 **비율과 통일감**을 유지한다.
- **개별 강조 요소 정렬**: `.key-message`, `.summary` 같은 강조 요소가 `.content`(flex-column) 안에서 불필요하게 늘어나거나(stretch) 서로 달라붙지 않도록 `align-self: center;` 와 `--gap` 변수를 통해 독립적인 숨쉴 공간을 반드시 확보한다.

## 3. 레퍼런스 템플릿
`assets/templates/` 폴더의 CSS 파일이 곧 템플릿이다. 빌드 시 `-t <이름>`으로 선택하며, 생략하면 `minimal-tech-hero`가 폴백으로 적용된다.

| 파일명 | 스타일 | 추천 용도 | 미리보기 |
|---|---|---|---|
| `minimal-tech-hero` | 다크 그라데이션, 네온 악센트, 테크 컨퍼런스풍 | B2B 기술 발표, 제품 소개 | [미리보기](./example/minimal-tech-hero/index.html) |
| `flat-serif` | 명조체 제목, 플랫 디자인, 인디고 포인트, 편집 디자인풍 | 교육 자료, 용어집, 매거진 스타일 발표 | [미리보기](./example/flat-serif/index.html) |
