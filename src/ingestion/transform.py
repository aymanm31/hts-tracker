from src.ingestion.sections import get_section


def transform_row(raw_row: dict, sequence_index: int) -> dict:
    htsno = raw_row.get("htsno") or ""
    chapter = htsno[:2] if len(htsno) >= 2 else None
    section, section_name = get_section(int(chapter)) if chapter and chapter.isdigit() else (None, None)

    is_heading = bool(raw_row.get("superior")) or not htsno

    return {
        "htsno": htsno or None,
        "indent": int(raw_row.get("indent", 0)),
        "description": raw_row.get("description"),
        "superior": raw_row.get("superior") == "true",
        "units": raw_row.get("units") or [],
        "general_rate": raw_row.get("general") or None,
        "special_rate": raw_row.get("special") or None,
        "other_rate": raw_row.get("other") or None,
        "footnotes": raw_row.get("footnotes") or [],
        "quota_quantity": raw_row.get("quotaQuantity") or None,
        "additional_duties": raw_row.get("additionalDuties") or None,
        "chapter": chapter,
        "section": section,
        "is_heading": is_heading,
        "sequence_index": sequence_index,
        "raw_json": raw_row,
    }