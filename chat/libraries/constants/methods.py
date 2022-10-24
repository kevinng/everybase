"""Method Keys

Track the methods (and their version) used to process a piece of data.

Key format:

<Data Value Name>__<Method Name>__<Method Semver Version Number>
"""

# Simple equality match of string against data key to ascertain user's choice.
DATA_KEY_MATCH = 'DATA_KEY_MATCH'

# Match string against match keywords associated with the model, to determine
# the model matching the keyword.
MATCH_KEYWORD_TO_MODEL_MATCH = 'MATCH_KEYWORD_TO_MODEL_MATCH'

# User free-text input
FREE_TEXT_INPUT = 'FREE_TEXT'

# User numeric input
NUMERIC_INPUT = 'NUMERIC_INPUT'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (DATA_KEY_MATCH, DATA_KEY_MATCH),
    (MATCH_KEYWORD_TO_MODEL_MATCH, MATCH_KEYWORD_TO_MODEL_MATCH),
    (FREE_TEXT_INPUT, FREE_TEXT_INPUT),
    (NUMERIC_INPUT, NUMERIC_INPUT)
]