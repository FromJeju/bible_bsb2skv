<div align="center">

# 📖 새김역 성경 (SKV)

**Saegim Korean Version** *(별칭: Standard Korean Version · Steady Korean Version)* · [Berean Standard Bible (BSB)](https://berean.bible/) 기반 독자 한국어 번역 오픈 프로젝트

<kbd>✅ 66권 · 1,189장 · 31,086절 완역</kbd> · <kbd>📘 원문: BSB (Public Domain)</kbd> · <kbd>📦 포맷: JSON & XML</kbd> · <kbd>⚖️ 본문: CC BY-NC-ND 4.0</kbd> · <kbd>💻 코드: MIT</kbd>

[✨ 핵심 원칙](#-핵심-원칙) · [📊 번역 현황](#-번역-현황) · [📦 산출물 및 검증](#-산출물-및-검증) · [📚 문서 안내](#-문서-안내) · [🗂️ 저장소 구조](#️-저장소-구조) · [⚖️ 라이선스](#️-라이선스)

</div>

> [!NOTE]
> **새김역 성경(SKV)** 은 기존 한국어 성경 번역본을 열람·대조하지 않고, 퍼블릭 도메인 영문 원문인 **Berean Standard Bible (BSB)** 과 원어(Strong's / Interlinear) 정보만을 근거로 새롭게 번역해 **JSON** 및 **XML**로 제공합니다.

---

## ✨ 핵심 원칙

- **🔍 독자 번역 (Clean-room Translation)**: 기존 한국어 성경 번역본을 참고하거나 모방하지 않고 BSB 영문 본문과 원어 근거만으로 새로 번역합니다.
- **🤖 AI 활용 및 검수 체계**: 용어집(`glossary.csv`)과 번역 가이드(`TRANSLATION_GUIDE.md`)를 기준으로 초벌 번역과 자동 검증을 수행하고, 고위험 구절(`high_risk_verses.csv`)은 별도 구조 분석 후 검수합니다.
- **🗣️ 현대적이고 명료한 한국어**: 고어체 종결어미(`~지어다`, `~도다`, `~더라` 등)를 배제하고 중학생 수준에서도 자연스럽게 읽히는 문체로 번역합니다.
- **📜 원문 출처 및 명칭 준수**: [BSB 라이선스](https://berean.bible/licensing.htm) 및 [이용 약관](https://berean.bible/terms.htm)에 따라 파생 번역본 제목에는 공식 `Berean` 명칭을 사용하지 않습니다.

---

## 📊 번역 현황

| 구분 | 권 수 | 장 수 | 절 수 | 상태 |
| :--- | :---: | :---: | :---: | :---: |
| 📜 **구약 성경** (`GEN`–`MAL`) | 39권 | 929장 | 23,145절 | ✅ **완역 완료** |
| ✝️ **신약 성경** (`MAT`–`REV`) | 27권 | 260장 | 7,941절 | ✅ **완역 완료** |
| **📖 전체 합계** | **66권** | **1,189장** | **31,086절** | 🎯 **100% 완역** |

---

## 📦 산출물 및 검증

전체 66권 통합본과 권별 개별 파일이 `output/` 아래 **JSON** 및 **XML** 형식으로 빌드되어 있습니다.

| 구분 | 경로 | 설명 |
| :--- | :--- | :--- |
| 🟨 **통합 JSON** | [`output/json/skv_bible.json`](./output/json/skv_bible.json) | 전체 66권 통합 JSON 데이터 |
| 🟦 **통합 XML** | [`output/xml/skv_bible.xml`](./output/xml/skv_bible.xml) | 전체 66권 통합 XML 데이터 |
| 📂 **권별 파일** | [`output/json/`](./output/json/) · [`output/xml/`](./output/xml/) | `01_GEN` ~ `66_REV` 권별 파일 |

### 🛠️ 빌드 및 검증 실행

```bash
# 특정 권 검증 및 빌드 (예: 창세기)
python3 scripts/build_and_validate.py --book GEN

# 전체 66권 검증 및 통합 JSON/XML 빌드
python3 scripts/build_and_validate.py --all --combined
```

---

## 📚 문서 안내

| 문서 | 설명 |
| :--- | :--- |
| 📘 [`TRANSLATION_GUIDE.md`](./TRANSLATION_GUIDE.md) | 번역 원칙, 문체·표기 기준, JSON/XML 스키마, QA 체크리스트 |
| 🤝 [`CONTRIBUTING.md`](./CONTRIBUTING.md) | 기여자 동의 사항, 고위험 구절 분석 및 검수 절차 |
| 🏷️ [`glossary.csv`](./glossary.csv) | 핵심 신학 용어·인명·지명 표준 대조표 |
| ⚠️ [`high_risk_verses.csv`](./high_risk_verses.csv) | 기존 번역 기억 오염 방지를 위한 고위험 구절(`HR001`–`HR016`) 목록 |
| 🧾 [`TRANSLATION_LOG.md`](./TRANSLATION_LOG.md) | 권별 번역·검증·빌드 작업 이력 |

---

## 🗂️ 저장소 구조

```text
bible_bsb2skv/
├── 📄 LICENSE                # 본문(CC BY-NC-ND 4.0) 및 코드(MIT) 이중 라이선스
├── 📖 README.md              # 프로젝트 안내
├── 📘 TRANSLATION_GUIDE.md   # 번역 원칙 및 JSON/XML 스키마 가이드
├── 🤝 CONTRIBUTING.md        # 기여·검수 안내
├── 🧾 TRANSLATION_LOG.md     # 번역 및 검증 작업 로그
├── 🏷️ glossary.csv           # 핵심 용어 대조표
├── ⚠️ high_risk_verses.csv   # 고위험 구절 목록 및 완료 현황
├── 🔬 analysis/              # 고위험 구절(HR001–HR016) 문장 구조 분석 기록
├── 🛠️ scripts/               # BSB 추출, 검증, JSON/XML 빌드 스크립트
├── 📚 source/
│   └── bsb/                  # BSB 원문 데이터
├── ✏️ work/
│   ├── bsb/                  # 권별 BSB 작업용 JSON 및 통계
│   └── skv/                  # 권별 SKV 번역 작업본 JSON (66권)
└── 📦 output/
    ├── json/                 # 권별 JSON + 통합 skv_bible.json
    └── xml/                  # 권별 XML + 통합 skv_bible.xml
```

---

## ⚖️ 라이선스

이 저장소는 콘텐츠 유형에 따라 **이중 라이선스**를 적용합니다. 자세한 조건은 [LICENSE](./LICENSE)를 확인해 주세요.

| 대상 | 라이선스 | 핵심 조건 |
| :--- | :--- | :--- |
| 📖 **성경 번역 본문 및 데이터**<br>(`output/`, `analysis/`, `glossary.csv` 등) | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ko) | 저작자표시 · 비영리 · 변경금지 |
| 💻 **파싱·변환·검증 소스 코드**<br>(`scripts/` 등) | [MIT License](https://opensource.org/license/mit) | 저작권·허가 표시 조건으로 자유 이용·수정·배포 |

> [!IMPORTANT]
> 원문인 **Berean Standard Bible (BSB)** 은 퍼블릭 도메인(Public Domain) 저작물이며, 원저작자의 이용 약관에 따라 본 파생 번역본에는 공식 `Berean` 명칭을 사용하지 않습니다.
