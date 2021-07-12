from celery import shared_task
from chat import models
from relationships import models as relmods
from chat.tasks.save_new_demand import save_new_demand

@shared_task
def save_new_demand_version(
        match: relmods.Match,
        last_message: models.TwilioInboundMessage
    ):
    """Save a new version of the demand

    Parameters
    ----------
    match
        Match we're working on
    last_message
        Last TwilioInboundMessage of the 'discuss with buyer' sequence

    Returns
    -------
    New supply
    """
    old_supply = match.supply
    new_supply = save_new_demand(last_message, True)

    old_supply.next_version = new_supply
    old_supply.save()

    match.supply = new_supply
    match.save()

    return new_supply