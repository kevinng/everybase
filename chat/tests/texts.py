"""Expected response body text to assert against.

We do not use the same rendering technique to produce expected response body
text, because then - if the rendering technique breaks, the test cases will not
be able to catch them.
"""

DO_NOT_UNDERSTAND_OPTION = \
"""Sorry I do not understand.

Please enter a valid option."""