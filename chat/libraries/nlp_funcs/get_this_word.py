from typing import Tuple
from chat.libraries.nlp_funcs.is_space import is_space

def get_this_word(
        text: str,
        pos: int
    ) -> Tuple[str, int, int]:
    """If text[pos] points to a character of a word (i.e., a string separated
    from the strings on its left and right by a space), return the word.

    The word, along with its start and end positions are returned in a tuple in
    the format:

    (string, start_pos, end_pos)
    
    A space may be a ' ', '\\n', '\\t' or end of text.
    
    If text[pos] is a space or text is of length 0, return None.

    E.g., 'aaa bbb ccc'. If points to 'bbb', return 'bbb'. If points to 'aaa',
    return 'aaa'. If points to 'ccc', return 'ccc'.

    Last updated/tested: 28 April 2021, 11:00 PM

    Parameters
    ----------
    text
        Text to parse
    pos
        Position within text to return a continuous string of text around
    """

    if len(text) == 0 or pos >= len(text) or pos < 0 or is_space(text[pos]):
        return None

    string = ''
    start_pos = pos
    end_pos = -1

    # Get non-space text before pos
    for i in reversed(range(0, pos)):
        c = text[i]
        if not is_space(c):
            string = c + string
            start_pos = i
        else:
            break

    # Get non-space text at and after pos
    for i in range(pos, len(text)):
        c = text[i]
        if not is_space(c):
            string += c
        else:
            break

    end_pos = start_pos + len(string)

    return (string, start_pos, end_pos)