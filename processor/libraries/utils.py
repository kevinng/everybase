import csv
import math

import editdistance

import processor.libraries.constants as const

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

def get_start_position_of_previous_word(text, pos, space_tolerance=2):
    """Returns start position of previous word before space from position pos in
    text.

    We allow a tolerance for the number of consecutive spaces to be considered
    as a single space. This lets us tolerate human errors where more than 1
    spaces may be entered where the human meant to enter 1.

    Returns -1 if position is not found.

    E.g., 'aaa bbb ccc ddd eee'. If pos points to 'ccc', return start of 'bbb'.
    If pos points to 'bbb', return start of 'aaa'. If pos points to 'aaa',
    return start of 'aaa'.

    Last updated/tested: 29 April 2021, 9:48 PM

    Parameters
    ----------
    text
        Text to parse
    pos
        Position to parse from
    space_tolerance
        Number of consecutive spaces to be considered as a single space.
        Defaults to 2.
    """

    start_pos = pos
    space_count = 0
    for i in reversed(range(0, pos)):
        if is_space(text[i]):
            space_count += 1
        
        if space_count >= space_tolerance:
            break

        start_pos = i

    return start_pos

def get_end_position_of_next_word(text, pos, space_tolerance=2):
    """Returns position of the end of the next word after the immediate next
    space in text from position pos.

    We allow a tolerance for the number of consecutive spaces to be considered
    as a single space. This lets us tolerate human errors where more than 1
    spaces may be entered where the human meant to enter 1.

    Returns -1 if position is not found.

    E.g., 'aaa bbb ccc ddd eee'. If pos is pointing in 'ccc', we want to return
    one after the end of 'ddd'. If pos is pointing to 'ddd', we want to return
    one after the end of 'eee'. If pos is pointing to 'eee', we want to return
    one after the end of 'eee'.

    Last updated/tested: 29 April 2021, 3:50 PM

    Parameters
    ----------
    text
        Text to parse
    pos
        Position to parse from
    """

    end_pos = -1
    space_count = 0
    for i in range(pos, len(text)):
        if is_space(text[i]):
            space_count += 1
        
        end_pos = i
        
        if space_count >= space_tolerance:
            break

    if end_pos == len(text)-1:
        end_pos = len(text)
    
    return end_pos

def tlds():
    """Returns list of top-level domain (TLD) names.
    
    We store TLDs in a CSV file. The path to the file is configured via the
    constant _TLDS_PATH.
    
    We use the TLD list for operations like identifying URLs.

    Last updated/tested: 28 April 2021, 9:01 PM
    """

    tlds = []
    with open (const._TLDS_PATH) as f:
        rows = csv.reader(f, delimiter=',')
        next(rows, None) # Skip headers
        for r in rows:
            tlds.append(r[0][1:]) # Removes initial '.'
    return tlds

def is_tld(text):
    """Returns matching TLD if input text is a TLD.

    Returns None if input text is not a TLD.
    
    We use edit distance with 20% difference in threshold (rounded down). E.g.,
    for a 5 character-long TLD, matching 4 characters will trigger a match.

    The list of TLD is loaded in a separate function.

    Last updated: 29 April 2021, 8:48 PM

    Parameters
    ----------
    text
        Text to test if its a TLD
    """

    threshold = math.floor(len(text) * 0.2)
    for tld in tlds():
        if match(text, tld, threshold):
            return tld
    return None

def find_any(text, strings, start_pos=0):
    """Returns next position from start_pos of any string in input list strings.

    Returns -1 if none of the strings are found in text.

    E.g., 'aaa bbb ccc ddd eee'. If search for ['bbb', 'ddd'] will return
    start of 'bbb'. If search for ['ccc', 'ddd', 'eee'] from start_pos 11 will
    return start of 'ddd'.

    Last updated: 29 April 2021, 10:36 PM

    Parameters
    ----------
    text
        Text to search
    strings
        List of strings to search in text
    start_pos
        Position to start searching for
    """
    
    poss = []
    for s in strings:
        pos = text.find(s, start_pos)
        if pos != -1:
            poss.append(pos)

    return sorted(poss)[0] if len(poss) > 0 else -1

def get_first_word(text):
    """Returns the first word in text.

    Words are separated from other words by 1 or more spaces.

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

def get_this_word(text, pos):
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