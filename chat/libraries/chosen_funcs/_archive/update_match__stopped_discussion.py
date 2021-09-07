import pytz, datetime
from everybase.settings import TIME_ZONE
from chat.libraries.classes.context_logic import ContextLogic

def update_match__stopped_discussion(message_handler, data_value):
    """Updates match - stop discussion"""
    logic = ContextLogic(message_handler)
    sgtz = pytz.timezone(TIME_ZONE)
    match = logic.get_match()
    
    # Update match
    if logic.is_buying():
        match.buyer_stopped_discussion = datetime.datetime.now(sgtz)
        match.buyer_stopped_discussion_value = data_value
    else:
        match.seller_stopped_discussion = datetime.datetime.now(sgtz)
        match.seller_stopped_discussion_value = data_value
    match.save()