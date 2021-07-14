from celery import shared_task
from chat import models
from relationships import models as relmods
from chat.tasks.save_new_demand import save_new_demand

@shared_task
def save_new_demand_version(
        match_id: int,
        last_message_id: int
    ):
    """Save a new version of the demand

    Parameters
    ----------
    match_id
        ID of the match we're working on
    last_message
        Last TwilioInboundMessage of the 'discuss with buyer' sequence

    Returns
    -------
    New demand if successful
    """
    try:
        match = relmods.Match.objects.get(pk=match_id)
    except relmods.Match.DoesNotExist:
        return None

    try:
        last_message = models.TwilioInboundMessage.objects.get(
            pk=last_message_id)
    except models.TwilioInboundMessage.DoesNotExist:
        return None

    old_demand = match.demand
    new_demand = save_new_demand(last_message, True)

    old_demand.next_version = new_demand
    old_demand.save()

    match.demand = new_demand
    match.save()

    return new_demand