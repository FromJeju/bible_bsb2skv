#!/usr/bin/env python3
"""Validate SKV translations against BSB source data and build JSON/XML outputs."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

ROOT = Path(__file__).resolve().parent.parent
WORK_BSB_DIR = ROOT / "work" / "bsb"
WORK_SKV_DIR = ROOT / "work" / "skv"
OUT_JSON_DIR = ROOT / "output" / "json"
OUT_XML_DIR = ROOT / "output" / "xml"
GLOSSARY_CSV = ROOT / "glossary.csv"

ARCHAIC_PATTERNS = [
    r"하였느니라",
    r"할지어다",
    r"가로되",
    r"이르시되",
    r"하였더라",
    r"이니라\b",
    r"이로다\b",
]
ARCHAIC_RE = re.compile("|".join(ARCHAIC_PATTERNS))
TAG_LEAK_RE = re.compile(r"<[^>]+>|\\[cv]\s+\d+")


def load_glossary() -> list[dict]:
    if not GLOSSARY_CSV.exists():
        return []
    with GLOSSARY_CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def find_bsb_file(book_id: str) -> Path | None:
    matches = sorted(WORK_BSB_DIR.glob(f"*_{book_id.upper()}.json"))
    return matches[0] if matches else None


def find_skv_file(book_id: str) -> Path | None:
    matches = sorted(WORK_SKV_DIR.glob(f"*_{book_id.upper()}.json"))
    return matches[0] if matches else None


def init_template(book_id: str) -> None:
    bsb_file = find_bsb_file(book_id)
    if not bsb_file:
        sys.exit(f"BSB source file not found for {book_id}. Run scripts/extract_bsb.py first.")
    WORK_SKV_DIR.mkdir(parents=True, exist_ok=True)
    out_file = WORK_SKV_DIR / bsb_file.name
    if out_file.exists():
        sys.exit(f"Target file already exists: {out_file}")

    with bsb_file.open(encoding="utf-8") as f:
        bsb = json.load(f)

    skv = {
        "id": bsb["id"],
        "order": bsb["order"],
        "name": bsb["name_ko"],
        "testament": bsb["testament"],
        "chapters": [],
    }
    for ch in bsb["chapters"]:
        verses_out = []
        for v in ch["verses"]:
            entry = {"verse": v["verse"]}
            if v.get("heading_en"):
                entry["heading"] = ""
            entry["text"] = ""
            if v.get("footnotes_en"):
                entry["footnotes"] = ["" for _ in v["footnotes_en"]]
            verses_out.append(entry)
        skv["chapters"].append({"chapter": ch["chapter"], "verses": verses_out})

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(skv, f, ensure_ascii=False, indent=2)
    print(f"Created translation template: {out_file}")


def validate_book(bsb: dict, skv: dict, glossary: list[dict]) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []
    book_id = bsb["id"]

    bsb_chapters = {c["chapter"]: c["verses"] for c in bsb["chapters"]}
    skv_chapters = {c["chapter"]: c["verses"] for c in skv.get("chapters", [])}

    if set(bsb_chapters.keys()) != set(skv_chapters.keys()):
        missing = sorted(set(bsb_chapters) - set(skv_chapters))
        extra = sorted(set(skv_chapters) - set(bsb_chapters))
        if missing:
            errors.append(f"[{book_id}] 누락된 장: {missing}")
        if extra:
            errors.append(f"[{book_id}] 원문에 없는 장: {extra}")
        return errors, warnings

    for ch_num, bsb_verses in bsb_chapters.items():
        skv_verses = skv_chapters[ch_num]
        bsb_v_map = {v["verse"]: v for v in bsb_verses}
        skv_v_nums = [v["verse"] for v in skv_verses]

        if len(skv_v_nums) != len(set(skv_v_nums)):
            errors.append(f"[{book_id} {ch_num}] 중복된 절 번호 존재")

        skv_v_map = {v["verse"]: v for v in skv_verses}
        if set(bsb_v_map.keys()) != set(skv_v_map.keys()):
            missing_v = sorted(set(bsb_v_map) - set(skv_v_map))
            extra_v = sorted(set(skv_v_map) - set(bsb_v_map))
            if missing_v:
                errors.append(f"[{book_id} {ch_num}] 누락된 절: {missing_v}")
            if extra_v:
                errors.append(f"[{book_id} {ch_num}] 원문에 없는 절: {extra_v}")
            continue

        for v_num, bsb_v in bsb_v_map.items():
            skv_v = skv_v_map[v_num]
            text = (skv_v.get("text") or "").strip()
            if not text:
                errors.append(f"[{book_id} {ch_num}:{v_num}] 본문이 비어 있음")
                continue

            if TAG_LEAK_RE.search(text):
                errors.append(f"[{book_id} {ch_num}:{v_num}] 마크업/태그 잔여물 발견: {text[:60]}")

            if ARCHAIC_RE.search(text):
                warnings.append(f"[{book_id} {ch_num}:{v_num}] 고어체 어미 의심 표현 포함: {text[:60]}")

            if bsb_v.get("is_poetry") and "\n" in bsb_v.get("text_en", "") and "\n" not in text:
                warnings.append(f"[{book_id} {ch_num}:{v_num}] 시가서 원문에 줄바꿈이 있으나 번역문에 없음")

            if bsb_v.get("heading_en") and not (skv_v.get("heading") or "").strip():
                warnings.append(f"[{book_id} {ch_num}:{v_num}] 원문 소제목('{bsb_v['heading_en']}') 누락")

            # Check key divine-title glossary alignment
            text_en = bsb_v.get("text_en", "")
            for row in glossary:
                if row.get("category") == "신적호칭":
                    src = row["source_term"]
                    ko = row["korean_term"]
                    if re.search(rf"\b{re.escape(src)}\b", text_en) and ko not in text:
                        warnings.append(f"[{book_id} {ch_num}:{v_num}] 용어집 점검: '{src}' → '{ko}' 미포함")

    return errors, warnings


def clean_book_for_output(skv: dict) -> dict:
    chapters_out = []
    for ch in skv["chapters"]:
        verses_out = []
        for v in ch["verses"]:
            item = {"verse": int(v["verse"])}
            heading = (v.get("heading") or "").strip()
            if heading:
                item["heading"] = heading
            item["text"] = v["text"].strip()
            footnotes = [fn.strip() for fn in v.get("footnotes", []) if fn and fn.strip()]
            if footnotes:
                item["footnotes"] = footnotes
            verses_out.append(item)
        chapters_out.append({"chapter": int(ch["chapter"]), "verses": verses_out})

    return {
        "id": skv["id"],
        "order": int(skv["order"]),
        "name": skv["name"],
        "testament": skv["testament"],
        "chapters": chapters_out,
    }


def book_to_xml_element(book_obj: dict) -> ET.Element:
    book_el = ET.Element(
        "book",
        {
            "id": book_obj["id"],
            "order": str(book_obj["order"]),
            "name": book_obj["name"],
            "testament": book_obj["testament"],
        },
    )
    for ch in book_obj["chapters"]:
        ch_el = ET.SubElement(book_el, "chapter", {"number": str(ch["chapter"])})
        for v in ch["verses"]:
            if "heading" in v:
                h_el = ET.SubElement(ch_el, "heading")
                h_el.text = v["heading"]
            v_el = ET.SubElement(ch_el, "verse", {"number": str(v["verse"])})
            v_el.text = v["text"]
            for fn in v.get("footnotes", []):
                fn_el = ET.SubElement(v_el, "footnote")
                fn_el.text = fn
    return book_el


def write_pretty_xml(root_el: ET.Element, out_path: Path) -> None:
    raw = ET.tostring(root_el, encoding="utf-8")
    parsed = minidom.parseString(raw)
    pretty = parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    out_path.write_text(pretty, encoding="utf-8")
    # Re-parse to confirm well-formedness
    ET.parse(out_path)


def build_outputs(books_clean: list[dict], version: str, write_combined: bool) -> None:
    OUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
    OUT_XML_DIR.mkdir(parents=True, exist_ok=True)

    meta = {
        "id": "skv",
        "name": "새김역 성경",
        "language": "ko",
        "source": "Berean Standard Bible (Public Domain)",
        "license": "CC BY-NC-ND 4.0",
        "version": version,
    }

    for b in books_clean:
        prefix = f"{b['order']:02d}_{b['id']}"
        json_payload = {"metadata": meta, "book": b}
        with (OUT_JSON_DIR / f"{prefix}.json").open("w", encoding="utf-8") as f:
            json.dump(json_payload, f, ensure_ascii=False, indent=2)

        bible_el = ET.Element("bible", meta)
        bible_el.append(book_to_xml_element(b))
        write_pretty_xml(bible_el, OUT_XML_DIR / f"{prefix}.xml")

    if write_combined and books_clean:
        combined_json = {"metadata": meta, "books": books_clean}
        with (OUT_JSON_DIR / "skv_bible.json").open("w", encoding="utf-8") as f:
            json.dump(combined_json, f, ensure_ascii=False, indent=2)

        bible_el = ET.Element("bible", meta)
        for b in books_clean:
            bible_el.append(book_to_xml_element(b))
        write_pretty_xml(bible_el, OUT_XML_DIR / "skv_bible.xml")


def main():
    parser = argparse.ArgumentParser(description="Validate SKV translations and build JSON/XML outputs.")
    parser.add_argument("--init-template", metavar="BOOK", help="Create empty SKV translation template for BOOK (e.g. JHN)")
    parser.add_argument("--book", metavar="BOOK", help="Validate and build a single book (e.g. JHN)")
    parser.add_argument("--all", action="store_true", help="Validate and build all books present in work/skv/")
    parser.add_argument("--combined", action="store_true", help="Also write combined skv_bible.json and skv_bible.xml")
    parser.add_argument("--version", default="0.1.0", help="Metadata version string")
    args = parser.parse_args()

    if args.init_template:
        init_template(args.init_template)
        return

    glossary = load_glossary()
    targets = []
    if args.book:
        p = find_skv_file(args.book)
        if not p:
            sys.exit(f"No SKV file found for {args.book} in {WORK_SKV_DIR}")
        targets.append(p)
    elif args.all:
        targets = sorted(WORK_SKV_DIR.glob("*.json"))
        if not targets:
            sys.exit(f"No SKV files found in {WORK_SKV_DIR}")
    else:
        parser.print_help()
        return

    all_errors = []
    all_warnings = []
    books_clean = []

    for skv_path in targets:
        with skv_path.open(encoding="utf-8") as f:
            skv = json.load(f)
        bsb_path = find_bsb_file(skv["id"])
        if not bsb_path:
            all_errors.append(f"Missing BSB source for {skv['id']}")
            continue
        with bsb_path.open(encoding="utf-8") as f:
            bsb = json.load(f)

        errs, warns = validate_book(bsb, skv, glossary)
        all_errors.extend(errs)
        all_warnings.extend(warns)
        if not errs:
            books_clean.append(clean_book_for_output(skv))

    for w in all_warnings:
        print(f"WARN: {w}")
    for e in all_errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if all_errors:
        sys.exit(f"\nValidation failed with {len(all_errors)} error(s).")

    books_clean.sort(key=lambda x: x["order"])
    build_outputs(books_clean, version=args.version, write_combined=args.combined)
    print(f"Validated and built {len(books_clean)} book(s) -> output/json/ and output/xml/")


if __name__ == "__main__":
    main()
