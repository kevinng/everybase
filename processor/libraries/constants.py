# Path to CSV file with a list of TLDs for matching
TLDS_PATH = './processor/libraries/data/tld.csv'












# WE LIKELY WON'T NEED TAGS ANYMORE - because we will be marking positions
# in the string


# ***** Tags *****
# TODO swap these in
"""
Tags are used to mark (i.e., tag) words in text. We use the XML format for
tagging so we may leverage on existing XML parsing libraries.

However, we ALLOW overlapping tags as it's POSSIBLE for entities to share words
with adjacent text. E.g.,

<a><b>xxx</a> yyy</a>

We have to be careful when parsing. E.g., remove all tags in an entity before
using it.

We put tags in a dictionary to faciliate the checking of the existance of
tags by iterating through the dictinoary name.
"""
TAGS = {
    # Dots
    'DOT__FULLSTOP__STARTEND': '<dot type="fullstop"/>',
    'DOT__DOMAIN__STARTEND': '<dot type="domain"/>',
    # Decimals and thousand separators
    'DECIMAL__DOT__STARTEND': '<decimal type="dot"/>',
    'DECIMAL__COMMA__STARTEND': '<decimal type="comma"/>',
    'THOUSAND_SEPARATOR__DOT__STARTEND': '<thousand_separator type="dot"/>',
    'THOUSAND_SEPARATOR__COMMA__STARTEND': '<thousand_separator type="comma"/>',
    # Emails
    'EMAIL__START': '<email>',
    'EMAIL__END': '</email>',
    'EMAIL__POSSIBLE__START': '<email type="possible">',
    'EMAIL__SUSPICIOUS__START': '<email type="suspicious">',
    # Tags for testing purposes
    'TESTING_ONLY__START': '<testing_only>',
    'TESTING_ONLY__END': '</testing_only>',
    'TESTING_ONLY__STARTEND': '<testing_only/>'
}