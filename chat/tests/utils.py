from chat import models

def create_mock_message(user, body):
    """Create mock TwilioInboundMessage for the purposes of testing.

    Parameters
    ----------
    user : relationships.User
        User sending this message
    body : string
        Message body
    """
    return models.TwilioInboundMessage.objects.create(
        from_user=user,
        body=body
    )