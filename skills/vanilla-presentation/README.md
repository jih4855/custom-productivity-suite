# Vanilla Presentation Skill

이 시스템은 외부 라이브러리(Impress.js 등) 없이 **순수 HTML/CSS/JS**만을 사용하여 비즈니스 스타일의 프리젠테이션을 제작하고 자동화하기 위한 스킬 세트입니다.

## 제작 원칙 (Core Principles)
- **Visual-First**: 슬라이드는 시각적 보조 자료일 뿐입니다. 본문 내용은 발표자의 말이 담당하며, 슬라이드에는 **표·다이어그램·이미지**와 핵심 키워드만 담습니다.
- **One Slide, One Message**: 한 장에 너무 많은 정보를 담지 않습니다. (컴포넌트 최대 2개 제한)
- **Fixed Frame**: 프레임은 고정하고 내용만 바꿈으로써 전체 문서의 통일성을 유지합니다.
- **Zero Runtime Dependency**: 외부 프레젠테이션 라이브러리나 CDN 없이, 생성된 HTML/CSS/JS 파일 묶음을 브라우저에서 실행합니다.

## 폴더 구조 (Directory Structure)
```text
vanilla-presentation/
├── assets/
│   ├── build.py          # JSON 스펙을 기반으로 HTML을 조립하는 빌드 엔진
│   ├── css/
│   │   └── base.css      # 모든 슬라이드의 공통 레이아웃 프레임 정의
│   ├── js/
│   │   └── engine.js     # 슬라이드 내비게이션 및 엔진 로직
│   ├── templates/
│   │   └── *.css         # 공식 테마 카탈로그 (normal-style.css 등)
│   └── examples/
│       └── */            # 테마별 전수 컴포넌트 시각적 가이드 (index.html)
├── SKILL.md              # AI 에이전트 전용 상세 작동 명세서
└── README.md             # 사용자 및 에이전트를 위한 통합 안내서
```

## AI 에이전트 사용 가이드 (For LLMs)
이 스킬을 사용하는 에이전트는 다음의 **강제 워크플로우**를 따릅니다:

1.  **사전 협의**: 작업을 시작하기 전, 반드시 사용자에게 **디자인 방향(테마)**과 **슬라이드 구성**을 제안하고 승인을 받습니다.
2.  **예제 검증**: 테마를 새로 만들거나 수정할 경우, `assets/examples/`에 갤러리를 생성하여 사용자에게 시각적 피드백을 먼저 받습니다.
3.  **Bottom-up 튜닝**: 결과물이 나온 뒤 세부 디자인을 수정할 때는 생성된 `theme.css`를 먼저 고쳐서 확정받은 뒤, 원본 템플릿에 역반영합니다.

## 사용 방법 (Usage)
1.  `spec.json`을 작성하여 슬라이드 내용과 구조를 정의합니다.
2.  아래 명령어를 실행하여 빌드합니다:
    ```bash
    python3 assets/build.py -s <경로/spec.json> -t <테마명> -o <경로/index.html>
    ```

## 커스터마이징 (Customization)
- **자유로운 수정**: 이 시스템은 사용자의 요구에 맞춰 유연하게 수정할 수 있도록 설계되었습니다. `base.css`를 고쳐 프레임을 바꾸거나, 새로운 CSS를 `templates/`에 추가해 본인만의 브랜딩을 구축하세요.
- **피드백 루프**: AI 에이전트에게 디자인 수정을 요청하면, 에이전트가 `SKILL.md` 지침에 따라 안전하게 반영합니다.
