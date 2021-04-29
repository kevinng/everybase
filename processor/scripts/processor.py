"""
Text markers are used to preprocess a body of text by tagging string of special
interest within the text body.

We use XML to specify text markers so we may leverage on existing XML parsers
for further processing.

Do not define text markers with spaces in them. This simplifies our checks for
spaces in text after we've inserted text markers.

Text markers:

<decimal_dot/> - A '.' character used as a decimal place as opposed to say, a 
    fullstop.
<domain_dot/> - A '.' used in a URL/domain name. E.g., URL, email
    address.
'<block_break/>' - A line break between 2 blocks of text.
"""

_TXTMARK_DECIMAL_DOT = '<decimal_dot/>'
_TXTMARK_DOMAIN_DOT = '<domain_dot/>'
_TXTMARK_BLOCK_BREAK = '<block_break/>'
_TXTMARK_EMAIL_START = '<email>'
_TXTMARK_EMAIL_END = '</email>'
_TXTMARK_EMAIL_POSSIBLE_START = '<email_possible>'
_TXTMARK_EMAIL_POSSIBLE_END = '</email_possible>'
_TXTMARK_EMAIL_SUSPICIOUS_START = '<email_suspicious>'
_TXTMARK_EMAIL_SUSPICIOUS_END = '</email_suspicious>'


import csv
import editdistance
import math

# Path to CSV file with a list of TLDs for matching
_TLDS_PATH = './processor/scripts/tld.csv'

def tlds():
    """Returns list of top-level domain (TLD) names.
    
    We store TLDs in a CSV file. The path to the file is configured via the
    local constant _TLDS_PATH.
    
    We use the TLD list for operations like identifying URLs.

    Last updated/tested: 28 April 2021, 9:01 PM
    """

    tlds = []
    with open (_TLDS_PATH) as f:
        rows = csv.reader(f, delimiter=',')
        next(rows, None) # Skip headers
        for r in rows:
            tlds.append(r[0][1:]) # Removes initial '.'
    return tlds

# def match(a, b, t):
#     """Returns True if the edit distance between input string a and input string
#     b is less than or equals to integer t.

#     Returns False otherwise.

#     Last updated/tested: 28 April 2021, 10:12 PM

#     Parameters
#     ----------
#     a
#         String A
#     b
#         String B
#     t
#         Edit distance threshold integer. Edit distance must be less than or
#         equals to t for string A to match string B.
#     """

#     return editdistance.eval(a, b) <= t

def find_nearest(text, strings, start_pos=0):
    """Returns position of the nearest (i.e., closest to 0) of any string in
    input list strings.

    Returns -1 if none of the strings are found in text.

    Last updated: 29 April 2021, 8:48 PM

    Parameters
    ----------
    text
        Text to search
    strings
        List of string to search in text
    start_pos
        Position to start searching for
    """
    
    poss = []
    for s in strings:
        pos = text.find(s, start_pos)
        if pos != -1:
            poss.append(pos)

    return sorted(poss)[0] if len(poss) > 0 else -1

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

def has_domain_dot_marker(text):
    """Returns True if text contains a domain dot text marker.

    Returns False otherwise.
    
    We use this as a simple check for various purposes - e.g., ascertaining if
    text is a URL, email, etc.

    Parameters
    ----------
    text
        Text to parse
    """

    return text.find(_TXTMARK_DOMAIN_DOT) != -1

# def is_space(c):
#     """Returns True if c is a space.

#     Returns False otherwise.

#     A space may be a ' ' or '\\t' or '\\n'.

#     Last updated/tested: 29 April 2021, 8:51 PM

#     Parameters
#     ----------
#     c
#         Character to test
#     """

#     return c is ' ' or c is '\t' or c is '\n'

# def get_first_string(text):
#     """Returns the first string in text before space.

#     Returns None if none found.

#     E.g., 'aaa bbb', returns 'aaa'. 'aaa' returns 'aaa'. ' bbb' or '' returns
#     None.

#     Last updated: 29 April 2021, 8:49 PM

#     Parameters
#     ----------
#     text
#         Text to parse
#     """

#     string = ''
#     for c in text:
#         if not is_space(c):
#             string += c
#         else:
#             break
#     return None if string == '' else string

def get_string_until_before_and_after_spaces(text, pos):
    """Returns continuous string of text from previous space to next space at
    text[pos] and start and positions in text where the string is found as a
    tuple in the format:

    (string, start_pos, end_pos)
    
    A space may be a ' ', '\\n', '\\t' or end of text.
    
    If text[pos] is a space or text is of length 0, return None.
    
    E.g., 'hello there world' and pos 7 returns 'there'. The same string with
    pos 3 returns 'hello'. The same string with pos 5 returns None.

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

def mark_string(string, start_pos, end_pos, start_tag, end_tag):
    """Returns marked string with tags at the start_pos and end_pos. The
    position of the character following the end_tag is also returned as part of
    a tuple in the format:

    (new_string, next_pos)

    Last updated/tested: 29 April 2021, 2:31 PM

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
        len(string[start_pos:end_pos]) + len(end_tag) + 1

    return (new_string, next_pos)

def words_around_position(text, start_pos, end_pos):
    """Returns word as position pos, and the words before/after this word
    separated by up to 2 spaces.

    If text[pos] is a space, returns words before/after this space. Including
    this space, the words before/after should not be separated by more than 2
    spaces.

    Returns None if no word is found.

    Parameters
    ----------
    text
        Text to parse
    pos
        Position to operate from
    """
    
    pass

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

def get_end_position_of_next_word(text, pos):
    """Returns position of the end of the next word after the immediate next
    space in text from position pos.

    We consider a continuous chain of 2 spaces as 1 space.

    Returns -1 if position is not found.

    E.g., 'aaa bbb ccc ddd eee'. If pos is pointing in 'ccc', we want to return
    the end of 'ddd'. If pos is pointing to 'ddd', we want to return the end
    of 'eee'. If pos is pointing to 'eee', we want to return the end of 'eee'.

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
        
        if space_count >= 2:
            break
    
    return end_pos

def mark_around_symbol(symbol_pos, symbol_len, text, start_tag, end_tag):
    """Returns marked text with start_tag/end_tag applied around symbol and its
    text; and the position after the end_tag as a tuple in the format:

    (marked_text, next_pos)

    If symbol has immediate text before it - mark the start of that text.
    If not, but there is a word before symbol (separated by up to 2 spaces),
    mark the start of that word.

    If symbol has immediate text after it - mark the end of that text. If
    not, but there is a word after symbol (separated by up to 2 spaces),
    mark the end of that word.

    In marking text, we have to be sure that we do not overlap
    TODO complete this sentence

    Parameters:
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
    """
    
    (string, string_start_pos, string_end_pos) = \
        get_string_until_before_and_after_spaces(text, symbol_pos)

    if string_start_pos == symbol_pos:
        # String obtained starts at symbol start position. So, we have no text
        # immediately before '@'. Thus, 'absorb' the word before the immediate
        # previous space into the start position.
        string_start_pos = \
            get_start_position_of_previous_word(text, string_start_pos)
    
    if string_end_pos == symbol_pos + symbol_len:
        # String obtained ends after symbol start position. So, we have no text
        # immediately after the symbol. Thus, 'absorb' the word after the
        # immediate next space into the end position.
        string_end_pos = get_end_position_of_next_word(text, string_end_pos)

    return mark_string(text, string_start_pos, string_end_pos, start_tag,
        end_tag)

def mark_emails(sentences):
    """Receives a list of dictionaries of sentences in get_sentence format.

    Mark dictionaries with the number of emails found in the sentence. E.g.,
    'email_count=1'.
    
    An email has an '@' symbol, followed by at least 1 domain dot marker in the
    string. The email string in the sentence is marked with text markers.

    Mark dictionaries with the number of possible emails found in the sentence.
    E.g., 'possible_email_count=1'.

    A possible email has the '@' symbol, but no domain dot markers following
    the string. The possible email string, which includes the '@' symbol and the
    words before/after it in the sentence are marked with text markers.

    Mark dictionaries with the number of suspicious emails found in the
    sentence. E.g., 'suspicious_email_count=1'.

    A suspicious email is a deliberate attempt to mask email addresses. Thus,
    we give it special attention. It has 1 or more of the the following symbols
    '(a)', '(at)', '[a]', '[at]'. The possible email string, which includes the
    symbol and the words before/after it in the sentence are marked with text
    markers.

    Last updated/tested: 29 April 2021, 12:18 PM

    Parameters
    ----------
    sentences
        List of dictionaries of sentences in get_sentence format
    """

    for s in sentences:
        this_sentence = s['sentence']
        
        # Find emails and possible emails
        email_count = 0
        possible_email_count = 0
        at_pos = this_sentence.find('@')
        while at_pos != -1:
            (email, email_start_pos, email_end_pos) = \
                get_string_until_before_and_after_spaces(this_sentence, at_pos)

            if has_domain_dot_marker(email):
                # String has domain (dot marker) - so is an email

                # Mark
                (s['sentence'], next_pos) = mark_string(this_sentence,
                    email_start_pos, email_end_pos,
                    _TXTMARK_EMAIL_START, _TXTMARK_EMAIL_END)

                email_count += 1
            else:
                # String has no domain (dot marker) - so is a possible email

                # Mark
                (s['sentence'], next_pos) = mark_around_symbol(at_pos, len('@'),
                    this_sentence, _TXTMARK_EMAIL_POSSIBLE_START,
                    _TXTMARK_EMAIL_POSSIBLE_END)

                possible_email_count += 1

            this_sentence = s['sentence']
            at_pos = this_sentence.find('@', next_pos)

        s['email_count'] = email_count
        s['possible_email_count'] = possible_email_count

        # Find suspicious emails
        suspicious_email_count = 0
        symbol = '(a)'
        at_pos = find_nearest(this_sentence, ['(a)', '[a]', '(at)', '[at]'])
        while at_pos != -1:
            # Mark
            (s['sentence'], next_pos) = mark_around_symbol(at_pos, len(symbol),
                this_sentence, _TXTMARK_EMAIL_SUSPICIOUS_START,
                _TXTMARK_EMAIL_SUSPICIOUS_END)

            this_sentence = s['sentence']
            at_pos = find_nearest(this_sentence, ['(a)', '[a]', '(at)', '[at]'],
                next_pos)

    return sentences

def mark_prices(sentences):
    """Receives a list of dictionaries of sentences in get_sentence format.

    Mark dictionaries where prices are found in the sentence with 


    Parameters
    ----------
    sentences
        List of dictionaries of sentences in the format initially produced by
        get_sentences

    Returns
    -------
    List of dictionaries of sentences in the same format as received, where
    each sentence with detected price elements - currency symbols, currency
    acronyms, price value - are marked in text.
    """
    pass

def mark_number_separators(text):
    """Mark decimal . and ,

    """

def get_sentences(text):
    """Break input text into sentences and return a list of dictionaries.

    Each dictionary in the list represents a sentence of a text.
    
    List order represents sentence order in text.

    E.g.,
    [
        {
            'sentence': 'hello world a@b.com'
        },
        {
            'sentence': 'foo bar a [at] b.com'
        }
    ]

    We call this output format the 'get_sentences' format.
    
    A sentence is not merely a newline. It may be terminated by a fullstop
    ('.'). We cannot simply split a line up by '.' because '.' is also used in
    other contexts - e.g., decimal, domain.

    Non-fullstop use of '.' is detected as follows:
        - Decimal place, numeric character before and after '.'
        - Domain name, top-level domain names after '.'

    Non-fullstop use of '.' are marked with text markers.

    Last updated/tested: 28 April 2021, 10:51 PM

    Parameters
    ----------
    text
        Input text.
    """

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

def get_most_likely_product_from_user(uom, incoterm_availability, location):
    """Where the user did not indicate the product he is selling, only the
    quantity, UOM, incoterms/availability, and/or location - we'd infer the
    product from the information provided.



    I think we need to query the database? Yes - we need to prepare data for
    this

    """
    pass

def get_lead_blocks(sentences):
    """Breaks a list of ordered sentences into sub-lists of 'lead blocks'. A
    'lead block' is a sub-list of sentences describing 1 lead. 


    TODO:
    - Consider reading supporting data from the database.
    ...
    """
    pass



def get_prices(text):
    """Get all prices in text. There may be more than 1 prices in text.
This should operate on a line basis
    Currency codes
    --------------
    USD
        United States Dollar. Where a $ symbol is used with no other indication
        of currency, the USD is assumed.

    Returns
    -------
    prices
        List of prices obtained. Each price is a dictionary with fields:
            - Amount, float
            - Currency, which should be tied to the database (e.g., via PK).
                Code calling this function should be responsible for matching
                currency codes for this function and in the database.
            - Character position in text where this price is found
    """

    # # Find $ symbol
    # d_pos = text.find('$')

    # if d_pos != -1:
    #     # $ symbol found

    #     # Search before the $ until a line break or a space following an
    #     # immediate space preceding the $ symbol for an indication of the dollar
    #     # type.
    #     this_pos = d_pos
    #     this_char = text[this_pos:this_pos+1]
    #     spaces_found = 0
    #     while this_char != '\n' and this_pos != -1 and spaces_found < 2:
    #         this_char = text[this_pos:this_pos+1]
    #         # if this_char == ' ':

    #         print(this_char)
    #         this_pos -= 1


    # print(dollar_pos)
    # print(text[dollar_pos:dollar_pos+10])


def get_supply_blocks(text):
    """Get supply blocks in text. A supply block is a block of text describing
    a supply. A text may contain 1 or more supplies.

    Parameters
    ----------
    text: str
        Text to parse

    Returns
    -------
    supply_blocks
        A list of supply blocks, each in the format:
            {

            }

            TO BE CONTINUED
    """
    pass

def run():
    text = "kevin@gmail.com Care sss@Essential Fannin xxx yy xxzz nirtile @ OTG UK  \nBoxes of 200s count \n\u00a317.50 per 200 + vat \n8000 x 200 medium\n6000 x 200 Small\n\nInspect [a] and pay \nPO to secure inspection. \nFirst come first serve basis. \nFor more information DM or email us at info@suffolkmedicalsupplies.co.uk"
    s = get_sentences(text)
    s = mark_emails(s)
    print(s)

    # for e in s:
        # if 'email_start_pos' in e:
            # print(e['sentence'][e['email_start_pos']:e['email_end_pos']])

