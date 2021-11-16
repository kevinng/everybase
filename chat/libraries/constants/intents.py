"""Intent keys"""

NO_INTENT = 'NO_INTENT' # User has no intent
REGISTER = 'REGISTER'
LOGIN = 'LOGIN'
CONTACT_REQUEST = 'CONTACT_REQUEST'

# Deprecated 3 Nov 21
# Active 31 Aug 21
# MENU = 'MENU'
# FIND_BUYERS = 'FIND_BUYERS'
# FIND_SELLERS = 'FIND_SELLERS'
# TALK_TO_HUMAN = 'TALK_TO_HUMAN'
# RECOMMEND = 'RECOMMEND'
# PAY = 'PAY'

# Deprecated 31 Aug 21
# SPEAK_HUMAN = 'SPEAK_HUMAN'
# EXPLAIN_SERVICE = 'EXPLAIN_SERVICE'
# NEW_SUPPLY = 'NEW_SUPPLY'
# NEW_DEMAND = 'NEW_DEMAND'
# DISCUSS_W_BUYER = 'DISCUSS_W_BUYER'
# DISCUSS_W_SELLER = 'DISCUSS_W_SELLER'
# QNA = 'QNA'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_INTENT, NO_INTENT),
    (REGISTER, REGISTER),
    (LOGIN, LOGIN),
    (CONTACT_REQUEST, CONTACT_REQUEST),
    
    # Active
    # (MENU, MENU),
    # (FIND_BUYERS, FIND_SELLERS),
    # (FIND_SELLERS, FIND_SELLERS),
    # (TALK_TO_HUMAN, TALK_TO_HUMAN),
    # (RECOMMEND, RECOMMEND),
    # (PAY, PAY),
    
    # Deprecated
    # (SPEAK_HUMAN, SPEAK_HUMAN),
    # (EXPLAIN_SERVICE, EXPLAIN_SERVICE),
    # (NEW_SUPPLY, NEW_SUPPLY),
    # (NEW_DEMAND, NEW_DEMAND),
    # (DISCUSS_W_BUYER, DISCUSS_W_BUYER),
    # (DISCUSS_W_SELLER, DISCUSS_W_SELLER),
    # (QNA, QNA)
]