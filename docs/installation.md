# 설치 안내

이 Skill의 사용자-facing 이름은 `앱 기획 스킬`입니다. 기존 설치 경로와 내부 식별자는 `app-spec-coach`로 유지됩니다.

## 권장 배포 형태

V1의 제품 본체는 GitHub 저장소에 있는 Codex Skill이다. 독립 설치 프로그램이나 사용자의 인증 키를 수집하는 서비스가 아니다.

## GitHub에서 설치 요청

저장소를 공개한 뒤 사용자는 Codex에 다음처럼 요청할 수 있다.

```text
이 GitHub 저장소의 .agents/skills/app-spec-coach 경로를 Skill로 내 Codex에서 사용할 수 있게 설치해줘.
저장소 주소는 GitHub에 공개한 app-spec-coach 저장소 주소야.
```

Codex가 저장소 Skill 설치 기능을 제공하는 환경에서는 해당 기능을 사용한다. 사용자가 직접 폴더를 복사해야 하는 환경이면 현재 Codex 공식 설치 안내에 맞춰 설치한다.

설치 후 확인:

```text
앱 기획해 보자. 재고관리 앱 아이디어가 있어.
```

새 대화에서 Skill이 발견되지 않으면 새 대화를 시작하거나 Codex를 다시 시작한다.

## 로컬 점검

```powershell
python .agents/skills/app-spec-coach/scripts/doctor.py .
python .agents/skills/app-spec-coach/scripts/validate_spec.py .
```

두 스크립트는 네트워크, API 키, 외부 Python 패키지를 요구하지 않는다.

## 개인정보·인증 주의

이 Skill은 사용자의 API 키나 OAuth 토큰을 요구하지 않는다. 예제와 테스트에는 실제 환자·고객·직원 식별정보를 넣지 않는다.
