def get_match_key(line_item) -> str:
    if line_item.htsno:
        return line_item.htsno
    return f"blank::{line_item.chapter}::{line_item.indent}::{line_item.description}"