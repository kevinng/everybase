"""Intent keys"""

NO_INTENT = 'NO_INTENT' # User has no intent
REGISTER = 'REGISTER'
LOGIN = 'LOGIN'
LEAD = 'LEAD'

# Choices for model fields
# Note: remember to makemigrations when updating this list
choices = [
    (NO_INTENT, NO_INTENT),
    (REGISTER, REGISTER),
    (LOGIN, LOGIN),
    (LEAD, LEAD)
]