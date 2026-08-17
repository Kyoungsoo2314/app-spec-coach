# 업데이트 안내

## 버전 확인

저장소 루트의 `VERSION`과 `CHANGELOG.md`를 확인한다.

```powershell
Get-Content -LiteralPath VERSION -Encoding UTF8
```

## Codex에 업데이트 요청

```text
내 앱 기획 스킬(app-spec-coach)을 이 GitHub 저장소의 최신 버전으로 업데이트해줘.
저장소 주소는 GitHub에 공개한 app-spec-coach 저장소 주소야.
```

업데이트 전 현재 프로젝트의 `AGENTS.md`, `.app-spec-coach/STATE.md`, SPEC, 기존 Skill을 보존한다. 업데이트가 기존 문서나 규칙을 덮어쓸 가능성이 있으면 먼저 사용자에게 알린다.

## 규칙 변경

다음 변경은 버전을 올리고 CHANGELOG에 기록한다.

- Skill의 트리거·비트리거 조건 변경
- SPEC LOCK 조건 변경
- 검증 상태 의미 변경
- 상태 파일 형식 변경
- 이미지 capability 실패 처리 변경

모델이 업데이트되었다는 이유만으로 Skill의 SPEC을 자동 변경하지 않는다. 행동 eval을 다시 실행하고 변경이 필요할 때만 규칙을 수정한다.

## V1 원칙

자동 업데이트 daemon은 V1 필수가 아니다. 사용자가 이해할 수 있는 요청과 확인 가능한 버전 기록을 우선한다.
