from src.summarize.formatting import format_location
from src.summarize.sectors import get_sector
from src.summarize.llm_summarize import llm_summarize_change

RATE_FIELD_LABELS = {
    "general_rate": "General (MFN) duty rate",
    "special_rate": "Special program rate",
    "other_rate": "Column 2 rate",
    "description": "Description",
}


def template_summarize_change(change: dict) -> str:
    location = format_location(change.get("chapter"), change.get("section"))
    htsno = change.get("htsno") or "(no HTS number)"
    description = change.get("description") or ""

    if change["change_type"] == "added":
        sector = get_sector(change.get("chapter"))
        return f"NEW LINE ADDED — {htsno}: \"{description}\" — {location} — Affects: {sector}"

    if change["change_type"] == "removed":
        sector = get_sector(change.get("chapter"))
        return f"LINE REMOVED — {htsno}: \"{description}\" — {location} — Affects: {sector}"

    if change["change_type"] == "field_changed":
        field_label = RATE_FIELD_LABELS.get(change["field_changed"], change["field_changed"])
        old_val = change.get("old_value") or "(blank)"
        new_val = change.get("new_value") or "(blank)"
        sector = get_sector(change.get("chapter"))
        return (
            f"RATE CHANGED — {htsno}: \"{description}\" — {location} — Affects: {sector}\n"
            f"    {field_label}: {old_val} → {new_val}"
        )

    return f"UNKNOWN CHANGE TYPE — {change}"

def summarize_change(change: dict) -> str:
    try:
        return llm_summarize_change(change)
    except Exception as e:
        print(f"[warning] AI summarization failed ({e}), falling back to template")
        return template_summarize_change(change)

def build_report(changes: list[dict]) -> str:
    if not changes:
        return "No HTS changes detected in this check."

    lines = [f"HTS Change Report — {len(changes)} change(s) detected\n"]
    for change in changes:
        lines.append(summarize_change(change))
        lines.append("")

    return "\n".join(lines)