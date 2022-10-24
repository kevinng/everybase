def replace_string(
        text: str,
        start_pos: int,
        end_pos: int,
        replacement: str
    ):
    """Replace string specified by start_pos and end_pos with replacement
    string."""
    new_text = text[:start_pos] + replacement + text[end_pos:]
    new_pos = start_pos + len(replacement)
    return (new_text, new_pos)