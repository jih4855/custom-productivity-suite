---
name: vanilla-presentation
description: Vanilla JS와 CSS를 활용하여 외부 라이브러리 없이 세련된 비즈니스 스타일의 프리젠테이션을 제작할 때 참고하는 스킬 가이드입니다.
---

# Premium Vanilla Presentation Skill

이 가이드는 무겁고 불안정한 외부 라이브러리를 배제하고, 순수 **Vanilla JS**와 CSS를 활용해 세련되고 모던한 화이트 톤의 SaaS 스타일 프리젠테이션을 구축하기 위한 **제작 원칙·워크플로우·시각 시스템**을 정리한 문서입니다.

> [!IMPORTANT]
> **0~3장(제작 원칙 / 폴더 구조 / 텍스트 원칙 / JSON 스펙)은 모든 발표 자료 작성에 선행되는 강제 규칙입니다.**
> 디자인 디테일(4장 이후)을 보기 전에 반드시 0~3장을 따른다.

---

## 0. 제작 원칙 (Workflow) — MUST READ

### 0.1 시각 우선, 본문은 발표가 맡는다
- 슬라이드는 **표·다이어그램·이미지** 위주로 시각 정보만 담는다.
- 설명·맥락·해설 등 대부분의 내용은 **발표자의 말**로 전달한다.
- 슬라이드에 문단(여러 문장)을 넣지 않는다. 문단이 들어가면 발표가 슬라이드 낭독으로 변질된다.

### 0.2 텍스트는 대주제·소주제로 한정, 한 문장으로
- 발표 대본을 받으면 **대주제와 소주제만 추출**한다.
- 추출한 항목은 **줄바꿈 없는 한 문장**으로 단순하게 표현한다.
- 자세한 줄바꿈 규칙은 [§2 텍스트 표현 원칙](#2-텍스트-표현-원칙) 참고.

### 0.3 JSON 스펙으로 구조 먼저, 내용은 나중에
- 사용자에게 발표 대본·요지를 받으면, **먼저 JSON으로 슬라이드 구조 스펙을 작성**한다.
- JSON에는 슬라이드별 `kicker`, `title`, `lead`(선택), `components`(cards / table / flow / map / contract / split / banner / image)와 이미지 경로 등을 명시한다.
- JSON 구조가 확정된 뒤에야 HTML/CSS로 옮긴다.
- JSON 템플릿은 [§3 JSON 스펙](#3-json-스펙으로-구조-잡기) 참고.

### 0.4 슬라이드 수와 구성은 사전 협의
- 본 작성 전 **사용자와 슬라이드 매수·구성 컴포넌트를 협의**한다.
- 슬라이드는 좌→우 1D 흐름으로 배치되며 별도의 그리드 좌표는 받지 않는다.
- 임의로 슬라이드를 늘리거나 컴포넌트를 추가하지 않는다.
- 사전 협의 항목 체크리스트:
  - [ ] 총 슬라이드 수와 발표 순서
  - [ ] 슬라이드별 대주제·소주제
  - [ ] **사용할 구성요소** — [§3.3 컴포넌트 카탈로그](#33-컴포넌트-카탈로그)에서 슬라이드별로 골라 합의
  - [ ] 테마 방향 — 사용자 요청, 레퍼런스 URL, 무드보드, 산업 톤을 바탕으로 맞춤형 CSS 방향 합의
  - [ ] 이미지·로고·차트 데이터 등 자산 경로 (있다면)

### 0.5 사용자 커스텀 룰
- 사용자가 "초기 세팅을 다르게 가고 싶다"라고 요청하면, 위 0.1~0.4를 그 사용자에 맞게 커스텀한다.
- 커스텀이 발생하면 **해당 deck 폴더 안에 `RULES.md`를 만들어 차이점을 기록**한다 (다음 세션에서 일관성 유지).

### 0.6 레퍼런스 기반 맞춤형 테마
- `templates/minimal-tech-hero.css`는 **공식 완성 테마가 아니라 구현 예제**다. 어떤 클래스가 어떤 HTML 구조를 받고, 모든 컴포넌트를 어떻게 빠짐없이 그리는지 보여주는 단일 레퍼런스로 사용한다.
- 새 발표를 만들 때는 사용자 요청, 레퍼런스 URL, 무드보드, 산업 톤을 바탕으로 **결과물 폴더의 `theme.css`를 맞춤형으로 작성**한다.
- `-t`를 생략하면 `minimal-tech-hero`가 폴백으로 복사되지만, 이는 테스트 빌드와 구조 확인용이다. 실 발표 자료는 맞춤형 `theme.css`를 권장한다.
- 맞춤형 테마 작성 시 `minimal-tech-hero.css`의 컴포넌트 커버리지를 기준으로 삼아 `cards`, `flow`, `table`, `timeline`, `banner`, `cta` 등 모든 지원 컴포넌트가 깨지지 않게 한다.
- 결과물에서 검증된 테마가 반복 사용 가치가 있으면 `templates/<주제명>.css`로 회수해 재사용 가능한 템플릿으로 관리한다.

### 0.7 슬라이드 한 장의 다섯 가지 핵심
- **슬라이드 한 장의 다섯 가지 핵심**: 제목 / 메시지 / 시각 자료 / 근거 / 결론.
- 한 장에 다섯 가지가 모두 들어갈 필요는 없으나, **발표 전체로 보면 다섯 가지가 모두 채워져야** 한다.

### 0.8 슬라이드 밀도 제어 (Max 2 Rule)
- **한 슬라이드의 `components` 배열에는 최대 2개까지만 사용 가능하다.**
- 3개 이상의 컴포넌트가 필요하다면 슬라이드를 나누어 메시지를 분산한다.
- 이는 프레젠테이션의 가독성과 시각적 집중도를 극대화하고, 레이아웃 붕괴를 원천 차단하기 위한 절대 원칙이다.

### 0.9 프레임 고정 원칙 — "내용은 바꿔도 프레임은 흔들지 않는다"
PPT 전체가 "한 문서"로 보이려면 **프레임이 모든 슬라이드에서 같은 자리에 있어야** 한다. 슬라이드마다 디자인을 새로 만들지 말고, **고정 레이아웃 안에서 내용만 바꾼다.**
**프레임은 base.css가, 디자인은 테마 CSS가 책임진다.**

---

## 1. 폴더 구조 및 워크플로우

### 1.1 스킬 자산 (이 폴더, 수정 신중)
- `assets/build.py`: JSON → HTML 자동 조립 CLI 스크립트. **스킬 폴더에서 직접 실행한다. 복사 불필요.**
- `assets/css/base.css`: 공용 프레임 골격. 빌드 시 결과물 폴더로 복사됨.
- `assets/js/engine.js`: 발표 내비게이션 엔진. 빌드 시 결과물 폴더로 복사됨.
- `templates/minimal-tech-hero.css`: 모든 컴포넌트 스타일 구현 예제. 빌드 시 기본 `theme.css`로 복사되지만, 실 발표에서는 결과물 폴더의 `theme.css`를 맞춤형으로 조정한다.

### 1.2 결과물 폴더
결과물은 **반드시** `<workspace>/projects/<deck-name>/`에 모은다.
- `spec.json`: 사용자이 작성하는 유일한 소스 파일. (슬라이드 구조와 내용 정의)
- `index.html`: 빌드 후 자동 생성되는 최종 HTML 파일.
- `base.css`, `theme.css`, `engine.js`: `index.html`이 참조하는 외부 에셋 파일. 외부 CDN이나 프레젠테이션 라이브러리는 사용하지 않는다.

### 1.3 워크플로우 (빌드 명령)
1. 대본/요지를 바탕으로 `spec.json`을 작성하고 승인을 받는다.
2. 아래 명령으로 빌드한다:
   ```bash
   python3 <suite-root>/skills/vanilla-presentation/assets/build.py \
     -s <workspace>/projects/<deck-name>/spec.json \
     -t <테마명> \
     -o <workspace>/projects/<deck-name>/index.html
   ```
3. 생성된 `<workspace>/projects/<deck-name>/theme.css`를 사용자 요청과 레퍼런스에 맞게 수정한다.

---

## 2. 텍스트 표현 원칙
- **HTML `<br/>` 절대 사용 금지.** 화면 폭에 따라 의미 단위가 깨진다. 길면 문장을 쪼개거나 `lead`로 내린다.
- `h1`/`h2` (제목): 한 문장, 줄당 26자 이하.
- `lead` (부제/설명): 한 문장 ~70자.
- `node h3` / `card strong` (nowrap 강제 요소): 한 단어~짧은 어구, 18자 이하. 텍스트가 넘치면 레이아웃이 깨진다.

---

## 3. JSON 스펙 및 카탈로그

### 3.1 스펙 스키마 예시
```json
{
  "deck": "발표 제목",
  "layout": { "stepW": 1320 },
  "slides": [
    {
      "id": "s1",
      "type": "cover",
      "kicker": "SECTION",
      "title": "슬라이드 제목",
      "subtitle": "부제",
      "presenter": "발표자 / 소속"
    },
    {
      "id": "s2",
      "type": "content",
      "title": "일반 슬라이드",
      "lead": "보조 설명",
      "components": [
        {
          "type": "cards",
          "items": [ { "title": "카드 1", "desc": "설명" } ]
        }
      ]
    }
  ]
}
```

### 3.2 슬라이드 타입 (`slides[].type`)
- `cover`: 표지
- `sectionDivider`: 장 구분
- `qna`: 마지막 Q&A
- `content` (혹은 빈 값): 일반 콘텐츠 (base.css의 `.stage` 5층 그리드 레이아웃 적용)

### 3.3 컴포넌트 카탈로그 (`components[].type`)
> 여기서 선언한 type이 그대로 HTML 클래스가 되며 테마 CSS가 이를 그린다.
- **구조/요약**: `toc`(목차), `summary`(요약 결론)
- **내용/데이터**: `cards`(항목 그리드), `flow`(순서 노드), `contract`(다단 노드), `split`(좌우 대비), `table`(수치표), `checklist`(점검), `timeline`(시간 흐름), `image`(사진/스크린샷), `video`(영상)
- **보조/강조**: `keyMessage`(핵심 1문장), `banner`(경고/안내 박스), `source`(출처), `cta`(행동 유도 버튼)

### 3.4 컴포넌트별 JSON 키 & CSS 클래스 매핑

> 경량 모델이 spec.json을 작성할 때 이 표만 보면 된다. `type` 값이 그대로 CSS 클래스가 된다.

| type (JSON) | JSON 키 | 생성 HTML 태그 | CSS 클래스 |
|---|---|---|---|
| `cards` | `items[].title`, `items[].desc` | `div.card > strong + span` | `.cards`, `.card` |
| `flow` | `items[].title`, `items[].desc` | `div.node > h3 + p` | `.flow`, `.node` |
| `contract` | `items[].title`, `items[].desc` | `div.node > h3 + p` | `.contract`, `.node` |
| `split` | `items[].title`, `items[].desc` | `div.path > strong + p` | `.split`, `.path` |
| `table` | `headers[]`, `rows[][]` | `table > thead/tbody` | `table`, `th`, `td` |
| `checklist` | `items[].text` | `ul > li.check-item` | `.checklist`, `.check-item` |
| `timeline` | `items[].date`, `items[].desc` | `div.timeline-item > strong + span` | `.timeline`, `.timeline-item` |
| `map` | `items[].title`, `items[].desc` | `div.map > .box > strong + span` | `.map`, `.box` |
| `image` | `src`, `alt` | `div.image-frame > img` | `.image-frame` |
| `video` | `src`, `autoplay`(opt), `loop`(opt), `controls`(opt) | `div.video-frame > video` | `.video-frame` |
| `toc` | `items[].title`, `items[].page` | `ul > li.toc-item > span + span` | `.toc`, `.toc-item` |
| `summary` | `text` | `div.summary > p` | `.summary` |
| `keyMessage` | `message` | `div.key-message` | `.key-message` |
| `banner` | `text`, `style` (info/warn) | `div.banner` | `.banner`, `.banner.info`, `.banner.warn` |
| `source` | `text` | `div.source` | `.source` |
| `cta` | `text`, `href` | `a.cta` | `.cta` |

---

## 4. 테마 CSS 작성 가이드

`minimal-tech-hero`는 단일 레퍼런스 템플릿이다. 프레임(클래스명·HTML 구조)은 고정하고, 실제 발표의 디자인(색상·폰트·간격·장식)은 결과물 폴더의 `theme.css`에서 사용자 맞춤형으로 작성한다.

> **테마 생성 시 주의사항 (전수 구현 원칙)**
> 새로운 CSS 테마를 생성할 때는 나중에 어떤 컴포넌트를 꺼내 쓰더라도 디자인이 깨지지 않도록 **[§3.4 컴포넌트별 JSON 키 & CSS 클래스 매핑](#34-컴포넌트별-json-키--css-클래스-매핑)에 명시된 모든 컴포넌트 스타일을 반드시 포함해야 한다.**
> 일부 컴포넌트만 구현하는 것은 금지되며, 이는 테마의 범용성과 안정성을 위한 강제 사항이다.

### 4.1 필수 구현 클래스 (전수 검사 대상)
아래 클래스는 build.py가 출력하는 HTML과 1:1 대응한다. 새 테마에서 **하나라도 누락되면 안 된다.**

```
/* 기본 구조 */  .step, .kicker, h1, h2, .lead
/* 특수 슬라이드 */  .cover-meta, .divider, .divider .chapter, .qna
/* 내용/데이터 */  .cards .card strong span, .flow .node h3 p,
                  .split .path strong p, table th td,
                  .checklist .check-item, .timeline .timeline-item,
                  .image-frame, .video-frame, .contract, .map .box, .toc .toc-item
/* 보조/강조 */  .key-message, .banner .banner.info .banner.warn,
                .source, .cta, .summary
```

### 4.2 여백(Spacing) 및 비율 시스템의 통일성
- **하드코딩 금지**: `gap: 32px`, `padding: 16px` 처럼 숫자를 직접 적지 않는다.
- **전역 변수 활용**: `base.css`에 정의된 표준 간격 토큰(`--gap-xs`, `--gap-sm`, `--gap-md`, `--gap-lg`, `--gap-xl`)을 테마 CSS 전반에 일관되게 적용하여 전체 템플릿의 **비율과 통일감**을 유지한다.
- **버튼 및 개별 요소 정렬**: `.cta` 같은 버튼 요소나 `.key-message` 등이 `.content`(flex-column) 안에서 불필요하게 늘어나거나(stretch) 서로 달라붙지 않도록 `align-self: center;` 와 `--gap` 변수를 통해 독립적인 숨쉴 공간을 반드시 확보한다.

### 4.3 레퍼런스 템플릿
현재 `templates/` 폴더에는 `minimal-tech-hero` 하나만 유지한다. 이 파일은 새 맞춤형 테마를 만들 때 참고하는 구현 예제이며, 빌드 시 `-t`를 생략하면 테스트 폴백으로 적용된다.

| 파일명 | 역할 | 추천 용도 | 비주얼 |
|---|---|---|---|
| `minimal-tech-hero` | 모든 컴포넌트 구현을 보여주는 레퍼런스 템플릿 | 맞춤형 `theme.css` 제작의 출발점, 테스트 빌드 폴백 | [미리보기](./assets/examples/minimal-tech-hero-demo/index.html) |

---

## 5. AI 에이전트 작업 지침 (AI Agent Workflow)

사용자가 발표 자료 생성을 요청할 때, 에이전트는 다음 단계를 준수하여 작업의 완결성과 수정 편의성을 제공한다.

### 5.1 작업 순서
1.  **사전 협의 및 승인 (Mandatory)**: 본 작업 전 반드시 사용자에게 디자인 방향성(사용자 요청·레퍼런스·산업 톤)과 슬라이드 구성(개수, 컴포넌트 배치)을 제안하고 **명시적인 승인**을 받는다. 임의로 설계를 진행하지 않는다.
2.  **JSON 설계**: 승인된 구조에 따라 [§3. JSON 스펙 가이드](#3-json-스펙-가이드)를 참고하여 `spec.json`을 먼저 생성한다.
3.  **빌드 실행**: `build.py`를 실행하여 `index.html`, `base.css`, `theme.css`, `engine.js`를 생성한다.
4.  **맞춤형 테마 CSS 구현 및 검증**: 결과물 폴더의 `theme.css`를 사용자 요청과 레퍼런스에 맞게 작성하고, `minimal-tech-hero.css`의 컴포넌트 커버리지를 기준으로 전수 검증한다.
5.  **결과 보고**: 생성된 파일 링크와 함께, **사용자가 직접 스타일을 튜닝할 수 있도록 구현된 테마 CSS 전체 코드를 별도의 코드 블록으로 제공한다.** (복사 유도)
### 5.2 세부 스타일 튜닝 (Fine-tuning)
결과물의 세부 디자인을 조정할 때는 다음의 **Bottom-up** 방식을 권장한다.
1.  **결과물 직접 수정 및 시각적 피드백**: 빌드된 결과물 폴더의 `theme.css`를 직접 수정하며 실시간으로 디자인을 확인하고, **사용자에게 시각적으로 확정(승인)을 받는다.**
2.  **재사용 여부 판단**: 사용자가 확정한 수정 사항 중 반복 사용 가치가 있는 테마만 `assets/templates/<주제명>.css`로 회수한다.
3.  **일관성 유지**: 이를 통해 프로젝트별 맞춤형 결과물과 재사용 가능한 템플릿 자산을 분리한다.

### 5.3 사용자 경험 (UX) 강화
- **수정 유도**: "스타일을 직접 수정하려면 결과물 폴더의 `theme.css`를 수정하면 됩니다." 라고 안내한다.
- **내비게이션 안내**: 좌우 화살표(←/→) 이동만 지원함을 명확히 안내한다.
