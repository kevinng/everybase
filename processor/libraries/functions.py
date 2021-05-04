import csv
import math

import editdistance

from processor.libraries.constants import TAGS, TLDS_PATH

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
    space_tolerance
        Number of consecutive spaces to be considered as a single space.
        Defaults to 2.
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
    with open (TLDS_PATH) as f:
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

def has_tag_dot_domain(text):
    """Returns true if text contains a tag for a dot domain.

    Returns false otherwise.
    
    We use this as a simple check for various purposes - e.g., ascertaining if
    text is a URL, email, etc.

    Parameters
    ----------
    text
        Text to parse
    """

    return text.find(TAGS['DOT__DOMAIN__STARTEND']) != -1

# We'd likely need to deprecate this method - if we're going with marking
# positions in the text instead of explicitly inserting tags
def mark_string(string, start_pos, end_pos, start_tag, end_tag):
    """Marks string at positions start_pos and end_pos with start_tag and
    end_tag respectively. I.e., enclose the sub-string from start_pos and
    end_pos with start_tag and end_tag.

    Returns marked string, and position one after the end of end_tag as a tuple
    in the format:
    
    (string, pos)

    Last updated/tested: 29 April 2021, 11:19 PM

    Parameters
    ----------
    string
        String to parse and return
    start_pos
        Start position to tag
    end_pos
        End position to tag
    start_tag
        Start text marker tag to use
    end_tag
        End text marker tag to use
    """

    new_string = string[:start_pos] + start_tag + string[start_pos:end_pos] + \
        end_tag + string[end_pos:]

    next_pos = len(string[:start_pos]) + len(start_tag) + \
        len(string[start_pos:end_pos]) + len(end_tag)

    return (new_string, next_pos)

# We'd likely need to deprecate this method - if we're going with marking
# positions in the text instead of explicitly inserting tags
def mark_around_symbol(symbol_pos, symbol_len, text, start_tag, end_tag,
    space_tolerance=2):
    """Marks symbol and its surrounding two words with start_tag and end_tag.
    
    Returns marked text with start_tag/end_tag applied around symbol and its
    text; and the position after the end_tag as a tuple in the format:

    (marked_text, next_pos)

    If the symbol has a word immediately before it (i.e., there is no space
    separting the symbol and that word) - insert start_tag before the start of
    that word.

    If there is a space separating a word before the - insert start_tag before
    the start of that word.

    If there is no word before symbol - insert start_tag before symbol. 

    If the symbol has a word immediately after it (i.e., there is no space
    separating the symbol and that word) - insert end_tag after the end of that
    word.
    
    If there is a space separating a word after the symbol - insert _endtag after
    that word.
    
    If there is no word after symbol - insert end_tag after symbol.

    E.g.,
    
    'aaa bbb ccc'. Marking on 'bbb' yields '<x>aaa bbb ccc</x>'.
    Marking on 'aaa' yields '<x>aaa bbb</x> ccc'. Marking on 'ccc' yields
    'aaa <x>bbb ccc</x>'. 'aaa'. Marking on 'aaa' yields '<x>aaa</x>'.
    
    'aaa bbbcccddd eee'. Marking on 'ccc' yields 'aaa <x>bbbcccddd</x> eee'.
    Marking on 'bbb' yields '<x>aaa bbbccc</x>ddd eee'.

    We allow a tolerance for the number of consecutive spaces to be considered
    as a single space. This lets us tolerate human errors where more than 1
    spaces may be entered where the human meant to enter 1.

    Parameters
    ----------
    symbol_pos
        Start position of symbol in text
    symbol_len
        Length of symbol
    text
        Text to parse
    start_tag
        Start tag to insert
    end_tag
        End tag to insert
    space_tolerance
        Number of consecutive spaces to be considered as a single space.
        Defaults to 2.
    """

    symbol = text[symbol_pos:symbol_pos+symbol_len]

    # Get this word. If symbol is part of a longer word, we'd get the entire
    # word.
    (this_word, string_start_pos, string_end_pos) = get_this_word(
        text, symbol_pos)

    if this_word.startswith(symbol) and string_start_pos != 0:
        # There is no word immediately before symbol and we're not at the start
        # of text. Get start of previous word.
        string_start_pos = \
            get_start_position_of_previous_word(text, string_start_pos,
                space_tolerance)
    
    if this_word.endswith(symbol) and string_end_pos != len(text):
        # There is no word immediately after symbol. Get end of next word.
        string_end_pos = get_end_position_of_next_word(text, string_end_pos,
            space_tolerance)

    return mark_string(text, string_start_pos, string_end_pos, start_tag,
        end_tag)

# We'd likely need to deprecate this method - if we're going with marking
# positions in the text instead of explicitly inserting tags
def mark_numbers(line, space_tolerance=1):
# WE WANT TO MARK THE WHOLE NUMBER, and what we read
    """
We mark all the numbers, and then there's the unit of measure

number must stand on its own

we want to read the number last
We want to mark as many attributes as possible before marking numeric values

annotate original text, and the value read
the original purpose is to actually






And then there's the currency

What makes a number a numebr?
If it's 3M - it could be mistaken for 3 meters
3m 1860 is the model number


If there is a dot and comma, how do we treat them?
We have to be sure that 

Mark all decimal and thousand separators in input text line and return
    marked text.

    We EXPECT input text line to represent text in a single line - i.e.,
    tokenized by the newline character '\n'.

    The US standard annotates numbers as follows:

    123,456.78

    The European standard annotates numbers as follows:

    123.456,78

    We differentiate them as follows:

    Where a symbol (i.e., '.' or ',') is found, we ascertain if it is used
    between 2 numbers. If it follows 3 digits, it is a thousand separator, if it
    follows 2 or less digits, it is a decimal.

    We allow a space tolerance when ascertaining if a symbol sits between 2
    digits. E.g., a space tolerance of 1 allows for up to 1 space between the
    symbol and both numbers. E.g., '9. 1' and '9 .1' passes, but '9 . 1' fails.

    We do NOT assume the usage of notation to be consistent throughout input
    text.

    We allow a tolerance for the number of consecutive spaces between '.' and
    number to be considered as no-space. This lets us tolerate human errors
    where 1 or more spaces may be entered between a '.' and a number.

    We do not work with a number more than once. E.g., 123.456.000 - the '.'
    between 123 and 456 will be considered a thousand separator. The '.' between
    456 and 000 will be considered a fullstop (i.e., left unmarked).

    E.g., <d/> is a decimal separator, <t/> is a thousand separator. Exact tags
    used depends on constant value at runtime.

    '123.00' -> '123<d/>00'
    '123,00' -> '123<d/>00'
    '123.000' -> '123<t/>000'
    '123,000' -> '123<t/>000'
    '123.456.789' -> '123<t/>456<t/>789'
    '123.456.78' -> '123<t/>456<t/>78'
    '123,456,78' -> '123<t/>456<t/>78'
    '123.456,78' -> '123<t/>456<d/>78'
    '123,456.78' -> '123<t/>456<d/>78'

    Parameters
    ----------
    text
        Text to parse
    """
    pass

# def mark_domain_dots(text):
#     """

#     """

def get_sentences(text):
# CONSIDER IF WE REALLY WANT TO BREAK SENTENCES BY . and !


    """Break input text into sentences and return a list of dictionaries.

    Each dictionary in the list represents a sentence in text.
    
    List order follows sentence order in text. We call this the 'standard'
    format.

    E.g.,

    [
        {
            'sentence': 'hello world a@b.com'
        },
        {
            'sentence': 'foo bar a [at] b.com'
        }
    ]
    
    A sentence is not merely a newline. It may be terminated by a fullstop
    ('.').
    
    However, we cannot simply split a line up by '.' because it's also used in
    other contexts - e.g., decimal, domain.

    Non-fullstop use of '.' is detected as follows:
        - Decimal place, numeric character before and after '.'
        - Domain name, top-level domain names after '.'

    Non-fullstop use of '.' are marked accordingly.

    Last updated/tested: 28 April 2021, 10:51 PM
    UPDATE UPDATE

    Parameters
    ----------
    text
        Input text.
    """





    #### CAN BE SEPARATED BY ! ALSO



    lines = [l.strip() for l in text.splitlines()]

    # Replace '' with block break text marker
    lines = map(lambda l: _TXTMARK_BLOCK_BREAK if l == '' else l, lines)

    sentences = []

    # If '.' is not used between 2 numbers, it is a fullstop - break line up
    # into sentences.
    for l in lines:
        curr_pos = 0

        # Replace all '.' used between two numeric values with decimal text
        # markers
        for i, c in enumerate(l):
            if c == '.':
                if i < len(l)-1:
                    # '.' is not the last character (second-last is okay).
                    if i != 0 and \
                        l[i-1].isnumeric() and \
                        l[i+1].isnumeric():
                        # This is a decimal place, replace this '.' with decimal
                        # text marker


                        # If there are 2 numbers or less behind this '.' and no
                        # more, then this is a decimal place.

                        # If there are 3 numbers behind this, then this is a
                        # thousands separator.


# TODO improve this

                        l = l[:i] + _TXTMARK_DECIMAL_DOT + l[i+1:]
                    else:
                        # A TLD is the last unit of text in a URL. E.g., for
                        # google.com.sg, .sg is the TLD. So, we want to get the
                        # full string to the next space, split it by '.', and
                        # get the last chunk of text.
                        s = get_first_string(l[i:])
                        last_chunk = s.split('.')[-1]
                        tld = is_tld(last_chunk)
                        if tld != None:
                            # Last chunk of text is a TLD, replace all instances
                            # of '.' from position i to next space with text
                            # marker.
# TODO improve this
                            l = l[:i] + s.replace('.', _TXTMARK_DOMAIN_DOT) + \
                                l[i+len(s):]

        # (Safely) tokenize line with '.'
        line_sentences = [s for s in l.split('.') if len(s) > 0]

        sentences += line_sentences

        # Wrap sentences in dictionary to faciliate further processing
        wrapped = []
        for s in sentences:
            wrapped.append({'sentence': s})

    return wrapped