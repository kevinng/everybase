from chat import models

def get_latest_value(intent_key, message_key, data_key, user, inbound=True):
    """Get latest value captured in context (i.e., message_key, intent_key) with
    specified data key associated with either an inbound or outbound message

    Parameters
    ----------
    intent_key : String
        Intent key for context
    message_key : String
        Message key for context
    data_key : String
        Data key for data type
    user : relationships.User
        User for whom we're getting a value for
    inbound : Boolean
        If true, look for values associated with inbound messages. Otherwise,
        look for values associated with outbound messages.
    """
    # Get latest inbound/outbound context
    if inbound:
        dataset = models.MessageDataset.objects.filter(
            intent_key=intent_key,
            message_key=message_key,
            user=user.id,
            in_message__isnull=False
        ).order_by('-created').first()
    else:
        dataset = models.MessageDataset.objects.filter(
            intent_key=intent_key,
            message_key=message_key,
            out_message__isnull=False
        ).order_by('-created').first()

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
