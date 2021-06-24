"""Intent keys"""

NO_INTENT = 'NO_INTENT' # Where user has no intent

MENU = 'MENU'

SPEAK_HUMAN = 'SPEAK_HUMAN'
EXPLAIN_SERVICE = 'EXPLAIN_SERVICE'
REGISTER = 'REGISTER'
NEW_SUPPLY = 'NEW_SUPPLY'
NEW_DEMAND = 'NEW_DEMAND'
DISCUSS_W_BUYER = 'DISCUSS_W_BUYER'
DISCUSS_W_SELLER = 'DISCUSS_W_SELLER'
QNA = 'QNA'
CONNECT_QUESTION = 'CONNECT_QUESTION'
CONNECT_ANSWER = 'CONNECT_ANSWER'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_INTENT, NO_INTENT),
    (MENU, MENU),
    (SPEAK_HUMAN, SPEAK_HUMAN),
    (EXPLAIN_SERVICE, EXPLAIN_SERVICE),
    (REGISTER, REGISTER),
    (NEW_SUPPLY, NEW_SUPPLY),
    (NEW_DEMAND, NEW_DEMAND),
    (DISCUSS_W_BUYER, DISCUSS_W_BUYER),
    (DISCUSS_W_SELLER, DISCUSS_W_SELLER),
    (QNA, QNA),
    (CONNECT_QUESTION, CONNECT_QUESTION),
    (CONNECT_ANSWER, CONNECT_ANSWER)
]