# Skills Index

Custom Productivity Suite에 포함된 공개용 생산성 스킬 목록입니다. 두 스킬 모두 로컬에서 실행 가능한 파일 기반 워크플로우를 전제로 하며, 실제 업무 데이터나 개인 산출물은 레포에 포함하지 않습니다.

## 도구 목록

### 1. [Vanilla Presentation](skills/vanilla-presentation/SKILL.md)
- **목적**: 비즈니스 스타일 프레젠테이션 제작 시스템
- **특징**: 순수 HTML/CSS/JS 기반, JSON 스펙 → HTML 자동 빌드, 좌우 방향키 이동, build.py는 순수 조립기(인라인 스타일 없음)
- **기본 제공 테마**: `minimal-tech-hero` (밝은 미니멀 SaaS풍), `flat-serif` (명조 + 플랫 편집 디자인풍)
- **포트폴리오 포인트**: 발표 자료를 오피스 파일 수작업이 아니라 재현 가능한 웹 산출물로 생성
- **운영 가이드**: [skills/vanilla-presentation/SKILL.md](skills/vanilla-presentation/SKILL.md)
- **CSS 템플릿 신규 생성 시 참조 파일**:
  | 파일 | 역할 |
  |---|---|
  | `SKILL.md` §0.6, §3.4 | 필수 클래스 매핑 및 컴포넌트 전수 구현 원칙 |
  | `THEME_GUIDE.md` | 테마 CSS 작성 가이드 (필수 클래스, 여백 시스템, 레퍼런스 비교표) |
  | `assets/css/base.css` | 프레임 고정 골격 (슬라이드 셸, 그리드, padding 규칙) |
  | `assets/templates/minimal-tech-hero.css` | 밝은 미니멀 SaaS 스타일 레퍼런스 |
  | `assets/templates/flat-serif.css` | 명조+플랫 편집 디자인 스타일 레퍼런스 |
  | `example/master-spec.json` | 14종 컴포넌트 전수 테스트용 공유 데이터 |

### 2. [HTML to A4 PDF](skills/html-to-a4-pdf/SKILL.md)
- **목적**: 웹 기술을 활용한 A4 규격 문서 자동화 및 PDF 변환기
- **특징**: Chrome headless 기반, JSON 데이터 연동, 하드 페이지 레이아웃, 반복 문서 엔진 스캐폴딩
- **포트폴리오 포인트**: HTML/CSS 기반 문서를 실제 제출 가능한 A4 PDF로 자동 생성하는 워크플로우
- **운영 가이드**: [skills/html-to-a4-pdf/SKILL.md](skills/html-to-a4-pdf/SKILL.md)

## 공통 사용 가이드
모든 도구는 Python 3.9+ 환경을 필요로 하며, 각 폴더 내의 `SKILL.md`에서 세부 실행 명령어를 확인할 수 있습니다.
AI 에이전트와 작업할 때는 각 도구 폴더의 `SKILL.md`를 우선 참고하게 하십시오.

## 공개 레포 기준
- 커밋 대상: 스킬 문서, 공통 CSS/JS/Python 코어, 제네릭 예제
- 제외 대상: 실제 고객/개인 데이터, 로컬 `data.json`, 생성 PDF, 캐시, 로그, OS 메타 파일, 인증 파일
