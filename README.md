# 새김역 성경 (SKV)

[Berean Standard Bible (BSB)](https://berean.bible/) 영문 원문을 바탕으로 한국어로 독자 번역하여 **JSON** 및 **XML** 형식으로 제공하는 오픈 프로젝트입니다.

## 핵심 원칙

- **독자 번역(Clean-room Translation)**: 기존 한국어 성경 번역본을 열람·참고·대조하지 않고, BSB 영문 본문과 원어(Strong's / Interlinear) 정보만을 근거로 새롭게 번역합니다.
- **AI 본문 생성 금지**: AI 및 기계 번역기로 한국어 성경 본문을 생성·윤문하지 않으며, AI는 변환·검증 스크립트 작성 및 영문 문법 분석에만 제한적으로 사용합니다.
- **원문 출처**: 퍼블릭 도메인으로 공개된 [Berean Standard Bible (BSB)](https://berean.bible/licensing.htm)를 원문으로 사용하며, 원저작자의 [이용 약관](https://berean.bible/terms.htm)에 따라 파생 번역본 제목에는 공식 `Berean` 명칭을 사용하지 않습니다.

자세한 번역 기준과 참여 방법은 아래 문서를 참고해 주세요.

- [TRANSLATION_GUIDE.md](./TRANSLATION_GUIDE.md) — 번역 원칙, 문체·표기 기준, JSON/XML 스키마, QA 체크리스트
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 기여자 동의 사항, 고위험 구절 분석 및 검수 절차
- [high_risk_verses.csv](./high_risk_verses.csv) — 기존 번역 기억 오염 방지를 위해 사전 구조 분석이 필요한 구절 목록

## 저장소 구조

```text
bible_bsb2skv/
├── LICENSE                # 본문(CC BY-NC-ND 4.0) 및 코드(MIT) 라이선스
├── README.md              # 프로젝트 안내
├── TRANSLATION_GUIDE.md   # 번역 및 데이터 스키마 가이드
├── CONTRIBUTING.md        # 기여·검수 안내
├── high_risk_verses.csv   # 고위험 구절 목록
├── glossary.csv           # 인명·지명·핵심 용어 대조표 (예정)
├── analysis/              # 고위험 구절 문장 구조 분석 기록 (예정)
├── source/
│   └── bsb/               # BSB 원문 데이터
└── output/
    ├── json/              # 한국어 번역본 JSON 출력
    └── xml/               # 한국어 번역본 XML 출력
```

## 라이선스

이 저장소는 콘텐츠 유형에 따라 이중 라이선스를 적용합니다. 자세한 내용은 [LICENSE](./LICENSE)를 확인해 주세요.

- **성경 번역 본문 및 데이터**(`output/`, `analysis/`, `glossary.csv` 등): [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ko) (저작자표시-비영리-변경금지)
- **파싱·변환·검증 등 소스 코드**: [MIT License](https://opensource.org/license/mit)
