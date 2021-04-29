# Path to CSV file with a list of TLDs for matching
_TLDS_PATH = './processor/libraries/data/tld.csv'

# ***** Tags *****
# TODO swap these in
# Dots
_TAG__DOT__FULLSTOP__STARTEND = '<dot type="fullstop"/>'
_TAG__DOT__DOMAIN__STARTEND = '<dot type="domain"/>'
# Decimals and thousand separators
_TAG__DECIMAL__DOT__STARTEND = '<decimal type="dot"/>'
_TAG__DECIMAL__COMMA__STARTEND = '<decimal type="comma"/>'
_TAG__THOUSAND_SEPARATOR__DOT__STARTEND = '<thousand_separator type="dot"/>'
_TAG__THOUSAND_SEPARATOR__COMMA__STARTEND = '<thousand_separator type="comma"/>'
# Emails
_TAG__EMAIL__START = '<email>'
_TAG__EMAIL__END = '</email>'
_TAG__EMAIL__POSSIBLE__START = '<email type="possible">'
_TAG__EMAIL__SUSPICIOUS__START = '<email type="suspicious">'
# Tags for testing purposes
_TAG__TESTING_ONLY__START = '<testing_only>'
_TAG__TESTING_ONLY__END = '</testing_only>'
_TAG__TESTING_ONLY__STARTEND = '<testing_only/>'