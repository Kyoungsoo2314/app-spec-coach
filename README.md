# 앱 기획 스킬

앱 기획 스킬은 앱을 만들고 싶은 초보자의 막연한 설명을 대화로 정리해, 구현 가능한 `SPEC`과 검증 가능한 구현 계약으로 바꾸는 Codex Skill입니다. 사용자에게 보이는 이름은 `앱 기획 스킬`이고, 기존 설치·업데이트 호환성을 위해 내부 식별자와 저장소 이름은 `app-spec-coach`로 유지합니다.

이 저장소의 V1 제품은 독립 Windows/Mac 프로그램이 아니라 **GitHub에서 배포할 수 있는 Skill**입니다. Skill은 구현을 대신하는 범용 에이전트가 아니라 다음 연결을 책임집니다.

```text
막연한 앱 요청
→ 명세 충분성 판단
→ 쉬운 인터뷰
→ 모호함 감소
→ 업무 흐름·메뉴·화면 정리
→ 선택적 시각 검토
→ SPEC LOCK
→ 구현 계약
→ 실제 결과 검증
```

## 빠른 시작

### 1. 저장소 자체 점검

Python 표준 라이브러리만 있으면 됩니다.

```powershell
python .agents/skills/app-spec-coach/scripts/doctor.py .
python .agents/skills/app-spec-coach/scripts/validate_spec.py .
```

### 2. Codex에 설치 요청

GitHub에 공개한 뒤 새 Codex 대화에서 다음처럼 요청합니다.

```text
이 GitHub 저장소의 .agents/skills/app-spec-coach 경로를 Skill로 내 Codex에서 사용할 수 있게 설치해줘.
저장소 주소는 GitHub에 공개한 app-spec-coach 저장소 주소야.
```

Codex 환경에서 다른 저장소 Skill 설치 기능을 사용할 수 있으면 설치 과정을 처리합니다. 설치 후 새 Skill이 보이지 않으면 새 대화를 시작하거나 Codex를 다시 시작합니다. 이 저장소는 사용자가 인증 키를 복사해 붙여 넣게 하지 않습니다.

### 3. 첫 동작 확인

새 대화에서 다음 문장으로 시작합니다.

```text
앱 기획해 보자. 재고관리 앱 아이디어가 있어.
```

`앱 만들어줘`, `앱 기획 시작하자`, `이 아이디어를 앱으로 정리해 보자`처럼 같은 의도를 표현해도 됩니다.

정상적인 V1 동작은 바로 앱 코드를 작성하는 것이 아니라 다음 의미의 제안을 먼저 보여주는 것입니다.

> 아직 사용자, 업무 흐름, 저장할 정보와 완료 기준이 충분히 정해지지 않았습니다. 바로 만들기 전에 필요한 내용을 저와 간단히 정리해드릴까요?

그 다음 사용자가 동의하면 쉬운 선택형 질문, 현재 모호함, 업무 흐름, SPEC 초안 순서로 진행합니다.

## 이 Skill이 개입하는 경우

- “앱 기획해 보자”, “앱 만들어줘”, “이 업무를 프로그램으로 바꾸고 싶어”처럼 신규 앱 요구가 들어온 경우
- 기능은 많지만 사용자·업무 흐름·저장 정보·완료 기준이 비어 있는 경우
- 기존 SPEC을 검토하거나 빠진 결정만 찾고 싶은 경우
- 구현 후 결과가 확정 요구사항을 만족하는지 확인해야 하는 경우

## 개입하지 않는 경우

- 단순 버그 수정, 오타, 작은 스타일 변경
- 이미 확정된 SPEC의 단순 구현
- 리팩터링이나 테스트 하나 추가
- 앱 제작과 무관한 일반 코딩 요청

세부 기준은 [인터뷰 정책](.agents/skills/app-spec-coach/references/interview-policy.md)과 [공존 정책](.agents/skills/app-spec-coach/references/coexistence.md)을 참고합니다.

## 저장소 구조

```text
app-spec-coach/
├── SPEC.md
├── IMPLEMENTATION_CONTRACT.md
├── README.md
├── LICENSE
├── VERSION
├── CHANGELOG.md
├── .agents/skills/app-spec-coach/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── evals/
├── examples/
└── docs/
```

실제 앱 프로젝트에서 명세 코칭을 사용할 때는 앱 프로젝트 안에 기본적으로 다음 상태 문서를 둘 수 있습니다.

```text
.app-spec-coach/
├── STATE.md
├── SPEC.md
├── IMPLEMENTATION_CONTRACT.md
└── VERIFICATION.md
```

기존 프로젝트에 같은 목적의 문서 규칙이 있으면 그 규칙을 우선합니다.

## 중요한 설계 원칙

1. 사용자는 기술 용어 대신 실제 업무 상황으로 답합니다.
2. 한 번에 질문을 많이 던지지 않습니다. 기본은 1~3개, 새 주제의 첫 질문은 가능하면 1개입니다.
3. 모호함 수치는 정밀한 과학적 측정값이 아니라 대화 방향을 보여주는 약식 지표입니다.
4. 업무 흐름에서 메뉴와 화면을 도출하며, 사용자가 처음부터 메뉴를 추측하게 하지 않습니다.
5. 이미지 검토는 선택 사항입니다. 이미지에만 생긴 기능은 요구사항이 아닙니다.
6. 특정 모델 ID를 고정하지 않습니다. 구현과 이미지 생성은 현재 환경의 capability에 위임합니다.
7. `SPEC LOCK` 뒤의 추가 아이디어는 몰래 구현하지 않고 확장 후보로 기록합니다.
8. 실제로 실행하지 않은 검증은 `PASS`로 보고하지 않습니다.

## 현재 범위

V1에는 Skill, reference 규칙, 예제, 행동 eval, 설치·업데이트 문서, 표준 라이브러리 기반 점검 스크립트가 포함됩니다.

다음은 V1 비목표입니다.

- 독립 Windows/Mac 설치 프로그램
- 자체 로그인 또는 자체 LLM API 서버
- 자체 이미지 생성 서버
- 범용 다중 에이전트 오케스트레이터
- Plugin Directory 공개를 완료 조건으로 삼는 것

## 문서

- [최종 제품 명세](SPEC.md)
- [구현 계약](IMPLEMENTATION_CONTRACT.md)
- [설치 안내](docs/installation.md)
- [업데이트 안내](docs/update.md)
- [설계 철학](docs/philosophy.md)
- [문제 해결](docs/troubleshooting.md)
- [Codex 실행 프롬프트](docs/implementation-prompt.md)
- [수동 스모크 테스트](evals/manual-smoke-tests.md)
