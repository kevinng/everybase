from typing import TYPE_CHECKING, Union
from chat import models

if TYPE_CHECKING:
    from relationships import models as relmods

def get_latest_value(
        intent_key: str,
        message_key: str,
        data_key: str,
        user: 'relmods.User' = None,
        before_message: Union[models.TwilioInboundMessage,
            models.TwilioOutboundMessage] = None,
        after_message: Union[models.TwilioInboundMessage,
            models.TwilioOutboundMessage] = None,
        inbound=True
    ) -> models.MessageDataValue:
    """Get latest value captured in context (i.e., message_key, intent_key) with
    specified data key associated with either an inbound or outbound message.

    Parameters
    ----------
    intent_key
        Intent key for context
    message_key
        Message key for context
    data_key
        Data key for data type
    user
        User for whom we're getting a value for. None if message is outbound.
    before_message
        If specified, dataset should be created before this message
    after_message
        If specified, dataset should be created after this message
    inbound
        If true, look for values associated with inbound messages. Otherwise,
        look for values associated with outbound messages.
    """
    if user is None and inbound is True:
        raise Exception('User must be specified for values of inbound messages')

    dataset = models.MessageDataset.objects.filter(
        intent_key=intent_key,
        message_key=message_key
    )

    if inbound:
        dataset = dataset.filter(user=user.id, in_message__isnull=False)

        if before_message is not None:
            dataset = dataset.filter(
                in_message__created__lte=before_message.created)

        if after_message is not None:
            dataset = dataset.filter(
                in_message__created__gte=after_message.created)
    else:
        # User doesn't matter for outbound message
        dataset = dataset.filter(out_message__isnull=False)

        if before_message is not None:
            dataset = dataset.filter(
                out_message__created__lte=before_message.created)

        if after_message is not None:
            dataset = dataset.filter(
                out_message__created__gte=after_message.created)

    dataset = dataset.order_by('-created').first()

    if dataset is None:
        return None

    try:
        # Get value of dataset
        return models.MessageDataValue.objects.get(
            dataset=dataset,
            data_key=data_key
        )
    except models.MessageDataValue.DoesNotExist:
        return None