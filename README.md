<div align="center">

# 📖 새김역 성경 (SKV)

**Standard Korean Version** · [Berean Standard Bible (BSB)](https://berean.bible/) 기반 독자 한국어 번역 오픈 프로젝트

[[https://img.shields.io/badge/완역_현황-66권_1%2C189장_31%2C086절-10B981?style=for-the-badge&logo=bookstack&logoColor=white]](#-번역-현황)
[[https://img.shields.io/badge/원문-BSB_Public_Domain-2563EB?style=for-the-badge&logo=readthedocs&logoColor=white]](https://berean.bible/licensing.htm)
[[https://img.shields.io/badge/포맷-JSON_%26_XML-F59E0B?style=for-the-badge&logo=json&logoColor=white]](#-산출물-및-검증)
[[https://img.shields.io/badge/본문_라이선스-CC_BY--NC--ND_4.0-EF4444?style=for-the-badge&logo=creativecommons&logoColor=white]](./LICENSE)
[[https://img.shields.io/badge/코드_라이선스-MIT-14B8A6?style=for-the-badge&logo=opensourceinitiative&logoColor=white]](./LICENSE)

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
| 📜 **구약 성경** (`GEN`–`MAL`) | 39권 | 929장 | 23,145절 | [https://img.shields.io/badge/완역_완료-10B981?style=flat-square] |
| ✝️ **신약 성경** (`MAT`–`REV`) | 27권 | 260장 | 7,941절 | [https://img.shields.io/badge/완역_완료-10B981?style=flat-square] |
| **📖 전체 합계** | **66권** | **1,189장** | **31,086절** | [https://img.shields.io/badge/100%25_완역-2563EB?style=flat-square] |

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
