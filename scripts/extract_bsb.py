#!/usr/bin/env python3
"""Extract BSB USJ files into clean per-book JSON work files and corpus stats."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USJ_DIR = ROOT / "source" / "bsb" / "usj"
HIGH_RISK_CSV = ROOT / "high_risk_verses.csv"
WORK_BSB_DIR = ROOT / "work" / "bsb"
STATS_PATH = ROOT / "work" / "bsb_stats.json"

BOOKS = [
    ("GEN", 1, "창세기", "Genesis", "OT"),
    ("EXO", 2, "출애굽기", "Exodus", "OT"),
    ("LEV", 3, "레위기", "Leviticus", "OT"),
    ("NUM", 4, "민수기", "Numbers", "OT"),
    ("DEU", 5, "신명기", "Deuteronomy", "OT"),
    ("JOS", 6, "여호수아", "Joshua", "OT"),
    ("JDG", 7, "사사기", "Judges", "OT"),
    ("RUT", 8, "룻기", "Ruth", "OT"),
    ("1SA", 9, "사무엘상", "1 Samuel", "OT"),
    ("2SA", 10, "사무엘하", "2 Samuel", "OT"),
    ("1KI", 11, "열왕기상", "1 Kings", "OT"),
    ("2KI", 12, "열왕기하", "2 Kings", "OT"),
    ("1CH", 13, "역대상", "1 Chronicles", "OT"),
    ("2CH", 14, "역대하", "2 Chronicles", "OT"),
    ("EZR", 15, "에스라", "Ezra", "OT"),
    ("NEH", 16, "느헤미야", "Nehemiah", "OT"),
    ("EST", 17, "에스더", "Esther", "OT"),
    ("JOB", 18, "욥기", "Job", "OT"),
    ("PSA", 19, "시편", "Psalms", "OT"),
    ("PRO", 20, "잠언", "Proverbs", "OT"),
    ("ECC", 21, "전도서", "Ecclesiastes", "OT"),
    ("SNG", 22, "아가", "Song of Solomon", "OT"),
    ("ISA", 23, "이사야", "Isaiah", "OT"),
    ("JER", 24, "예레미야", "Jeremiah", "OT"),
    ("LAM", 25, "예레미야애가", "Lamentations", "OT"),
    ("EZK", 26, "에스겔", "Ezekiel", "OT"),
    ("DAN", 27, "다니엘", "Daniel", "OT"),
    ("HOS", 28, "호세아", "Hosea", "OT"),
    ("JOL", 29, "요엘", "Joel", "OT"),
    ("AMO", 30, "아모스", "Amos", "OT"),
    ("OBA", 31, "오바댜", "Obadiah", "OT"),
    ("JON", 32, "요나", "Jonah", "OT"),
    ("MIC", 33, "미가", "Micah", "OT"),
    ("NAM", 34, "나훔", "Nahum", "OT"),
    ("HAB", 35, "하박국", "Habakkuk", "OT"),
    ("ZEP", 36, "스바냐", "Zephaniah", "OT"),
    ("HAG", 37, "학개", "Haggai", "OT"),
    ("ZEC", 38, "스가랴", "Zechariah", "OT"),
    ("MAL", 39, "말라기", "Malachi", "OT"),
    ("MAT", 40, "마태복음", "Matthew", "NT"),
    ("MRK", 41, "마가복음", "Mark", "NT"),
    ("LUK", 42, "누가복음", "Luke", "NT"),
    ("JHN", 43, "요한복음", "John", "NT"),
    ("ACT", 44, "사도행전", "Acts", "NT"),
    ("ROM", 45, "로마서", "Romans", "NT"),
    ("1CO", 46, "고린도전서", "1 Corinthians", "NT"),
    ("2CO", 47, "고린도후서", "2 Corinthians", "NT"),
    ("GAL", 48, "갈라디아서", "Galatians", "NT"),
    ("EPH", 49, "에베소서", "Ephesians", "NT"),
    ("PHP", 50, "빌립보서", "Philippians", "NT"),
    ("COL", 51, "골로새서", "Colossians", "NT"),
    ("1TH", 52, "데살로니가전서", "1 Thessalonians", "NT"),
    ("2TH", 53, "데살로니가후서", "2 Thessalonians", "NT"),
    ("1TI", 54, "디모데전서", "1 Timothy", "NT"),
    ("2TI", 55, "디모데후서", "2 Timothy", "NT"),
    ("TIT", 56, "디도서", "Titus", "NT"),
    ("PHM", 57, "빌레몬서", "Philemon", "NT"),
    ("HEB", 58, "히브리서", "Hebrews", "NT"),
    ("JAS", 59, "야고보서", "James", "NT"),
    ("1PE", 60, "베드로전서", "1 Peter", "NT"),
    ("2PE", 61, "베드로후서", "2 Peter", "NT"),
    ("1JN", 62, "요한일서", "1 John", "NT"),
    ("2JN", 63, "요한이서", "2 John", "NT"),
    ("3JN", 64, "요한삼서", "3 John", "NT"),
    ("JUD", 65, "유다서", "Jude", "NT"),
    ("REV", 66, "요한계시록", "Revelation", "NT"),
]

POETRY_MARKERS = {"q1", "q2", "qr", "qa"}
HEADING_MARKERS = {"s1", "s2", "ms"}
SKIP_MARKERS = {"h", "toc1", "toc2", "toc3", "mt1", "b"}


def load_high_risk() -> set[tuple[str, int, int]]:
    hr = set()
    if not HIGH_RISK_CSV.exists():
        return hr
    with HIGH_RISK_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            book = row["book"].strip()
            ch = int(row["chapter"])
            v_start = int(row["verse_start"])
            v_end = int(row["verse_end"])
            for v in range(v_start, v_end + 1):
                hr.add((book, ch, v))
    return hr


def flatten_text(nodes) -> str:
    parts = []
    for item in nodes:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            t = item.get("type")
            if t in ("char", "ref"):
                parts.append(flatten_text(item.get("content", [])))
            elif t == "note":
                continue
    return " ".join("".join(parts).split())


def extract_note(note_node: dict) -> str:
    parts = []
    for item in note_node.get("content", []):
        if isinstance(item, dict) and item.get("marker") == "fr":
            continue
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            parts.append(flatten_text(item.get("content", [])))
    return " ".join("".join(parts).split())


def extract_book(book_id: str, order: int, name_ko: str, name_en: str, testament: str, hr_set: set):
    usj_path = USJ_DIR / f"{book_id}.usj"
    with usj_path.open(encoding="utf-8") as f:
        data = json.load(f)

    chapters = []
    current_ch = None
    current_verse = None
    pending_heading = []
    pending_cross_ref = []
    pending_superscription = []

    def flush_verse():
        nonlocal current_verse
        if current_verse is not None and current_ch is not None:
            lines = [ln.strip() for ln in current_verse.pop("_lines") if ln.strip()]
            current_verse["text_en"] = "\n".join(lines) if current_verse["is_poetry"] else " ".join(lines)
            if not current_verse["footnotes_en"]:
                current_verse.pop("footnotes_en")
            if not current_verse["heading_en"]:
                current_verse.pop("heading_en")
            if not current_verse["cross_ref_en"]:
                current_verse.pop("cross_ref_en")
            if not current_verse["superscription_en"]:
                current_verse.pop("superscription_en")
            current_ch["verses"].append(current_verse)
            current_verse = None

    for node in data.get("content", []):
        if not isinstance(node, dict):
            continue
        ntype = node.get("type")
        marker = node.get("marker")

        if ntype == "chapter":
            flush_verse()
            pending_heading.clear()
            pending_cross_ref.clear()
            pending_superscription.clear()
            current_ch = {"chapter": int(node["number"]), "verses": []}
            chapters.append(current_ch)
            continue

        if ntype != "para" or current_ch is None:
            continue

        if marker in SKIP_MARKERS:
            continue
        if marker in HEADING_MARKERS:
            txt = flatten_text(node.get("content", []))
            if txt:
                pending_heading.append(txt)
            continue
        if marker == "r":
            txt = flatten_text(node.get("content", []))
            if txt:
                pending_cross_ref.append(txt)
            continue
        if marker == "d":
            txt = flatten_text(node.get("content", []))
            if txt:
                pending_superscription.append(txt)
            continue

        is_poetry_para = marker in POETRY_MARKERS
        line_buf = []

        def flush_line():
            nonlocal line_buf
            if current_verse is not None:
                s = " ".join("".join(line_buf).split())
                if s:
                    current_verse["_lines"].append(s)
            line_buf = []

        for item in node.get("content", []):
            if isinstance(item, str):
                line_buf.append(item)
            elif isinstance(item, dict):
                itype = item.get("type")
                if itype == "verse":
                    flush_line()
                    flush_verse()
                    v_num = int(item["number"])
                    current_verse = {
                        "verse": v_num,
                        "heading_en": " / ".join(pending_heading) if pending_heading else "",
                        "cross_ref_en": " ".join(pending_cross_ref) if pending_cross_ref else "",
                        "superscription_en": " ".join(pending_superscription) if pending_superscription else "",
                        "is_poetry": is_poetry_para,
                        "is_high_risk": (book_id, current_ch["chapter"], v_num) in hr_set,
                        "_lines": [],
                        "footnotes_en": [],
                    }
                    pending_heading.clear()
                    pending_cross_ref.clear()
                    pending_superscription.clear()
                elif itype == "note":
                    if current_verse is not None:
                        note_txt = extract_note(item)
                        if note_txt:
                            current_verse["footnotes_en"].append(note_txt)
                elif itype in ("char", "ref"):
                    line_buf.append(flatten_text(item.get("content", [])))

        if current_verse is not None and is_poetry_para:
            current_verse["is_poetry"] = True
        flush_line()

    flush_verse()

    return {
        "id": book_id,
        "order": order,
        "name_ko": name_ko,
        "name_en": name_en,
        "testament": testament,
        "chapters": chapters,
    }


def main():
    WORK_BSB_DIR.mkdir(parents=True, exist_ok=True)
    hr_set = load_high_risk()

    total_chapters = 0
    total_verses = 0
    total_hr = 0
    books_summary = []

    for book_id, order, name_ko, name_en, testament in BOOKS:
        book_data = extract_book(book_id, order, name_ko, name_en, testament, hr_set)
        out_file = WORK_BSB_DIR / f"{order:02d}_{book_id}.json"
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        ch_count = len(book_data["chapters"])
        v_count = sum(len(c["verses"]) for c in book_data["chapters"])
        hr_count = sum(1 for c in book_data["chapters"] for v in c["verses"] if v["is_high_risk"])
        total_chapters += ch_count
        total_verses += v_count
        total_hr += hr_count
        books_summary.append({
            "order": order,
            "id": book_id,
            "name_ko": name_ko,
            "testament": testament,
            "chapters": ch_count,
            "verses": v_count,
            "high_risk_verses": hr_count,
        })

    stats = {
        "total_books": len(BOOKS),
        "total_chapters": total_chapters,
        "total_verses": total_verses,
        "total_high_risk_verses": total_hr,
        "books": books_summary,
    }
    with STATS_PATH.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(BOOKS)} books, {total_chapters} chapters, {total_verses} verses ({total_hr} high-risk).")


if __name__ == "__main__":
    main()
