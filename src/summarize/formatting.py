def format_location(chapter: str, section: str) -> str:
    if chapter and section:
        return f"Chapter {chapter} (Section {section})"
    elif chapter:
        return f"Chapter {chapter}"
    return "Unknown location"