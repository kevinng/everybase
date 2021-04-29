import editdistance

def is_space(c):
    """Returns True if c is a space.

    Returns False otherwise.

    A space may be a ' ' or '\\t' or '\\n'.

    Last updated/tested: 29 April 2021, 8:51 PM

    Parameters
    ----------
    c
        Character to test
    """

    return c is ' ' or c is '\t' or c is '\n'

def get_first_string(text):
    """Returns the first string in text before space.

    Returns None if none found.

    E.g., 'aaa bbb', returns 'aaa'. 'aaa' returns 'aaa'. ' bbb' or '' returns
    None.

    Last updated: 29 April 2021, 8:49 PM

    Parameters
    ----------
    text
        Text to parse
    """

    string = ''
    for c in text:
        if not is_space(c):
            string += c
        else:
            break
    return None if string == '' else string

def match(a, b, t):
    """Returns True if the edit distance between input string a and input string
    b is less than or equals to integer t.

    Returns False otherwise.

    Last updated/tested: 28 April 2021, 10:12 PM

    Parameters
    ----------
    a
        String A
    b
        String B
    t
        Edit distance threshold integer. Edit distance must be less than or
        equals to t for string A to match string B.
    """

    return editdistance.eval(a, b) <= t

def get_start_position_of_previous_word(text, pos):
    """Returns position of the start of previous word after the immediately
    previous space in text from position pos.

    We consider a continuous chain of 2 spaces as 1 space.

    Returns -1 if position is not found.

    E.g., 'aaa bbb ccc ddd eee'. If pos is pointing in 'ccc', we want to return
    the start of 'bbb'. If pos is pointing to 'bbb', we want to return the start
    of 'aaa'. If pos is pointing to 'aaa', we want to return the start of 'aaa'.

    Last updated/tested: 29 April 2021, 3:50 PM

    Parameters
    ----------
    text
        Text to parse
    pos
        Position to parse from
    """

    start_pos = pos
    space_count = 0
    for i in reversed(range(0, pos)):
        if is_space(text[i]):
            space_count += 1
        
        if space_count >= 2:
            break

        start_pos = i

    return start_pos