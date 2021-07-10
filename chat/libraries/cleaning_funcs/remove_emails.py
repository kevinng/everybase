from typing import Tuple
from chat.libraries.constants import tags
from chat.libraries.nlp_funcs.get_this_word import get_this_word
from chat.libraries.nlp_funcs.mark_string import mark_string
from chat.libraries.nlp_funcs.replace_string import replace_string
from chat.libraries.nlp_funcs.mark_clean_text import mark_clean_text

def remove_email(
        text: str,
        replacement: str = '*'
    ) -> Tuple[str]:
    """Remove emails from text

    Returns
    -------
    Tuple with cleaned text, marked text and list of position tuples:

    (cleaned_text, marked_text, positions)
    """
    # Find all email's start/end positions
    positions = []
    pos = 0
    while pos < len(text):
        pos = text.find('@', pos, len(text))
        if pos != -1:
            _, start_pos, end_pos = get_this_word(text, pos)
            positions.append((start_pos, end_pos))
            pos = end_pos
        else:
            break

    return mark_clean_text(
        text, positions, tags.EMAIL_START, tags.EMAIL_END, replacement)