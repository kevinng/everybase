from typing import Tuple

def mark_string(
        text: str,
        start_pos: int,
        end_pos: int,
        start_tag: str,
        end_tag: str
    ) -> Tuple[str, int]:
    """Marks text at positions start_pos and end_pos with start_tag and
    end_tag respectively. I.e., enclose the sub-string from start_pos and
    end_pos with start_tag and end_tag.

    Last updated/tested: 29 April 2021, 11:19 PM

    Parameters
    ----------
    Text
        Text to parse and return
    start_pos
        Start position to tag
    end_pos
        End position to tag
    start_tag
        Start text marker tag to use
    end_tag
        End text marker tag to use

    Returns
    -------
    Marked string and position one after the end of end_tag in a tuple:
    
        (text, pos)
    """

    new_text = text[:start_pos] + start_tag + text[start_pos:end_pos] + \
        end_tag + text[end_pos:]

    next_pos = len(text[:start_pos]) + len(start_tag) + \
        len(text[start_pos:end_pos]) + len(end_tag)

    return (new_text, next_pos)