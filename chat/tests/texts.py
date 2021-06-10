"""Expected response body text to assert against.

We do not use the same rendering technique to produce expected response body
text, because then - if the rendering technique breaks, the test cases will not
be able to catch them.
"""

DO_NOT_UNDERSTAND_OPTION = \
"""Sorry I do not understand.

Please enter a valid option."""

DISCUSS_W_SELLER__STILL_INTERESTED__CONFIRM = \
"""Are you still interested in nitrile gloves?

*Reply*:
1. Yes
2. No"""

DISCUSS_W_SELLER__DISCUSS__CONFIRM_DETAILS = \
"""*Your demand*:

Nitrile Gloves
Israel
12000 Boxes
200 pieces in 1 box
Target USD 15.15 per box

*Are your demand details correct?*
1. Yes
2. No"""