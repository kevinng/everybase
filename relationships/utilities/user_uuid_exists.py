from relationships import models

def user_uuid_exists(uuid: str):
    """Returns User model reference if user with UUID exists. None otherwise."""
    try:
        user = models.User.objects.get(uuid=uuid)
    except models.User.DoesNotExist:
        return None

    if isinstance(user, models.User):
        return user

    return None