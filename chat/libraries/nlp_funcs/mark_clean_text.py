from typing import List, Tuple
from chat.libraries.nlp_funcs.mark_string import mark_string
from chat.libraries.nlp_funcs.replace_string import replace_string

def mark_clean_text(
        text: str,
        positions: List[Tuple[int, int]],
        start_tag: str,
        end_tag: str,
        replacement: str
    ) -> Tuple[str, str, List[Tuple[int, int]]]:
    """positions is a list of tuple - each with the start and end positions of
    a string to 'mark'. Each string in text is marked by being enclosed with
    the start_tag and end_tag. 2 versions of the original input text is
    produced:

        1. cleaned_text - which has all instances of the strings marked out by
            positions replaced with the replacement string
        2. marked_text - which has all instances of the strings marked out by
            positions enclosed by the start_tag and end_tag

    Returns
    -------
    Tuple with cleaned text, marked text and list of position tuples:

    (cleaned_text, marked_text, positions)
    """
    # Mark and clean text
    marked_text = '%s' % text # Copy
    cleaned_text = '%s' % text # Copy
    # Positions are sorted, start from the largest position
    for start_pos, end_pos in reversed(positions):
        marked_text, _ = mark_string(
            marked_text, start_pos, end_pos, start_tag, end_tag)
        cleaned_text, _ = replace_string(
            cleaned_text, start_pos, end_pos, replacement)

    return (cleaned_text, marked_text, positions)