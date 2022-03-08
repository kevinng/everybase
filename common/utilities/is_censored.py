import re
from email_scraper import scrape_emails

_shareable_forbidden_words = [
    'call me',
    'email me',
    'email',
    'facebook',
    'mail',
    'phone',
    'phones',
    'telegram',
    'viber',
    'we chat',
    'wechat',
    'whats app',
    'whatsapp',
    'you tube',
    'youtube',
    '微 信',
    '微信',
]

def is_censored(body):
    """Returns True if body text is censored. False otherwise."""
    if body is None:
        return False

    # Check for emails
    emails = scrape_emails(body)
    if len(emails) > 0:
        return True

    # Account for case differences
    lbody = body.lower()

    # Defeat efforts to replace keywords
    replacement_words = [('one', '1'), ('two', '2'), ('three', '3'), 
        ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'),
        ('eight', '8'), ('nine', '9'), ('zero', '0'), ('plus', '+'),
        ('dot', '.'), ('dash', '-')]

    pbody = lbody
    for r in replacement_words:
        pbody = pbody.replace(r[0], r[1])
    
    # Check for forbidden keywords
    forbidden_words = [
        '( a )',
        '( at )',
        '( dot )'
        '(a)',
        '(at)',
        '(dot)',
        '.au',
        '.ca',
        '.ch',
        '.co',
        '.com',
        '.de',
        '.edu',
        '.es',
        '.fr',
        '.gov',
        '.it',
        '.jp',
        '.me'
        '.mil',
        '.net',
        '.nl',
        '.no',
        '.org',
        '.ru',
        '.se',
        '.site',
        '.top',
        '.uk' ,
        '.us',
        '.xyz',
        '@',
        '[ a ]',
        '[ at ]',
        '[ dot ]',
        '[a]',
        '[at]',
        '[dot]',
        'http',
        'www',
    ] + _shareable_forbidden_words
    for w in forbidden_words:
        if pbody.find(w) != -1:
            return True

    # Extract tokens likely to be phone numbers
    token_chars = ['+', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ',
'-', '.'] # Token chars. A token is a string that contains only these chars.
    tokens = [] # Tokens extracted
    started = False # True if we're currently extracting a token in body text
    string = '' # Buffer token string that's currently being extracted
    for c in pbody:
        match = False # True if this characters matches a token characters
        for tc in token_chars:
            if c == tc:
                # Found characters that's a token characters
                match = True
                break # Stop matching against rest of token characters

        if match:
            # Found characters that's a token characters
            if not started:
                # Start extraction if we haven't
                started = True
            string += c # Extract
        else:
            # Found characters that's not a token characters
            if started:
                started = False
                string = string.strip()
                if len(string) > 7:
                    # Don't use tokens that're too short (in case regex matches against meaningful numbers).
                    # Phone numbers should need be above 7 characters, and it's not likely for a meaningful number to be above 10M-1.
                    tokens.append(string)
                string = ''

    # Extract a token at the end of the text body, which would not be extracted
    # by a trigger of finding a character that's not a token character.
    if started:
        string = string.strip()
        if len(string) > 7:
            # Don't use tokens that're too short (in case regex matches against meaningful numbers).
            # Phone numbers should need be above 7 characters, and it's not likely for a meaningful number to be above 10M-1.
            tokens.append(string)

    # Regular expressions matching phone numbers
    ph_regexs = [
        '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        '^\s*(?:\+?(\d{1,3}))?[\W\D\s]*(\d[\W\D\s]*?\d[\D\W\s]*?\d)[\W\D\s]*(\d[\W\D\s]*?\d[\D\W\s]*?\d)[\W\D\s]*(\d[\W\D\s]*?\d[\D\W\s]*?\d[\W\D\s]*?\d)(?: *x(\d+))?\s*$',
        '\s*(?:\+?(\d{1,3}))?[\W\D\s]^|()*(\d[\W\D\s]*?\d[\D\W\s]*?\d)[\W\D\s]*(\d[\W\D\s]*?\d[\D\W\s]*?\d)[\W\D\s]*(\d[\W\D\s]*?\d[\D\W\s]*?\d[\W\D\s]*?\d)(?: *x(\d+))?\s*$',
        '((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})',
        '^(1-)?\d{3}-\d{3}-\d{4}$',
        '^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
        '/^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d+)\)?)[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$/i',
        '^\(*\+*[1-9]{0,3}\)*-*[1-9]{0,3}[-. /]*\(*[2-9]\d{2}\)*[-. /]*\d{3}[-. /]*\d{4} *e*x*t*\.* *\d{0,4}$',
        '^([0-9\(\)\/\+ \-]*)$',
        '/^[+#*\(\)\[\]]*([0-9][ ext+-pw#*\(\)\[\]]*){6,45}$/',
        '/^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$/gm',
        '/(\+*\d{1,})*([ |\(])*(\d{3})[^\d]*(\d{3})[^\d]*(\d{4})/',
        '^((((\(\d{3}\))|(\d{3}-))\d{3}-\d{4})|(\+?\d{2}((-| )\d{1,8}){1,5}))(( x| ext)\d{1,5}){0,1}$',
        '((\+[0-9]{2})|0)[.\- ]?9[0-9]{2}[.\- ]?[0-9]{3}[.\- ]?[0-9]{4}',
        '^[0-9+\(\)#\.\s\/ext-]+$',
        '^(\\(?\\d\\d\\d\\)?)( |-|\\.)?\\d\\d\\d( |-|\\.)?\\d{4,4}(( |-|\\.)?[ext\\.]+ ?\\d+)?$',
        '\+?1?\s*\(?-*\.*(\d{3})\)?\.*-*\s*(\d{3})\.*-*\s*(\d{4})$',
        '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
        '^(\+?[01])?[-.\s]?\(?[1-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    ]

    # Match each phone number regular expression against each token
    for r in ph_regexs:
        for t in tokens:
            rx = re.compile(r)
            search = rx.findall(t)
            if len(search) > 0:
                return True

    return False