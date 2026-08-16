# Codex 구현 실행 프롬프트

아래 내용을 새 Codex 작업에 그대로 붙여 넣어 `app-spec-coach` 저장소를 구현·검증할 수 있다. 이미 저장소가 있다면 현재 파일과 프로젝트 규칙을 먼저 읽고, 없는 파일만 만든다.

```text
당신은 app-spec-coach라는 Codex Skill 기반 하네스를 구현한다.

목표는 초보 사용자가 “앱 만들어줘”라고 말했을 때 Codex가 빈칸을 임의로 채워 바로 코딩하지 않고, 먼저 쉬운 인터뷰를 제안하고, 요구사항을 개발 가능한 SPEC과 검증 가능한 구현 계약으로 바꾸게 하는 것이다.

진실의 기준:
1. 사용자의 요청과 명시적 승인
2. 현재 프로젝트의 AGENTS.md와 기존 규칙
3. LOCK된 SPEC
4. app-spec-coach의 일반 규칙
5. 추정

반드시 지킬 행동:
- 신규 앱 요청의 명세가 부족하면 “먼저 같이 정리할까요?”를 제안한다.
- 사용자가 동의하면 한 문장 재정의, 약식 모호함, 쉬운 선택형 질문 순서로 진행한다.
- 한 번에 기본 1~3개만 질문하고, 이미 답한 내용은 다시 묻지 않는다.
- 기술 스택 이름보다 실제 업무 상황을 묻는다.
- 업무 흐름에서 최소 메뉴·화면을 도출한다.
- 이미지 검토는 업무 흐름과 화면이 정리되고 사용자가 동의한 경우에만 선택적으로 제안한다.
- 이미지 생성은 현재 환경의 capability에 위임하며 특정 모델 ID를 핵심 규칙에 넣지 않는다.
- 이미지에만 있는 기능은 SPEC에 자동 추가하지 않는다.
- 이미지 capability가 없어도 텍스트 SPEC 흐름을 계속한다.
- 모호함 약 15% 이하와 핵심 결정 확인 전에는 SPEC을 LOCK하지 않는다.
- LOCK 후 추가 기능은 사용자 승인 전까지 구현하지 않고 확장 후보로 기록한다.
- LOCK 후에도 자동 구현하지 말고 구현 승인을 별도로 받는다.
- 실제 실행하지 않은 검증을 PASS라고 보고하지 않는다. 결과는 PASS, FAIL, NOT RUN, BLOCKED 중 하나다.
- 기존 AGENTS.md, 다른 Skill, 실행 하네스, 테스트와 공존하며 삭제·덮어쓰지 않는다.

필수 산출물:
- .agents/skills/app-spec-coach/SKILL.md
- references/interview-policy.md
- references/ambiguity-rubric.md
- references/risk-depth.md
- references/workflow-and-ui.md
- references/visual-review.md
- references/spec-template.md
- references/spec-lock.md
- references/implementation-contract.md
- references/verification-policy.md
- references/coexistence.md
- 표준 라이브러리만 사용하는 doctor.py와 validate_spec.py
- E01~E14 행동 eval
- 설치·업데이트·문제 해결 문서

비목표:
- 독립 Windows/Mac 앱
- 자체 인증·LLM API·이미지 서버
- 범용 에이전트 오케스트레이터
- Plugin Directory 공개를 V1 완료 조건으로 삼기

완료 전 실행:
python .agents/skills/app-spec-coach/scripts/doctor.py .
python .agents/skills/app-spec-coach/scripts/validate_spec.py .

두 명령의 실제 결과와 실행하지 못한 검증을 구분해 보고하고, 실행하지 않은 항목을 PASS로 바꾸지 않는다.
```

이 프롬프트는 현재 저장소의 `SPEC.md`와 `IMPLEMENTATION_CONTRACT.md`를 함께 읽을 때 가장 정확하게 작동한다.

