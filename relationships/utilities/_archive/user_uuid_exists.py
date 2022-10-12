from typing import Union
from relationships import models

def user_uuid_exists(
        uuid: str
    ) -> Union[bool, models.User]:
    """Returns User model reference if an existing user owns this UUID, False otherwise. Returns None if error.
    
    Parameters
    ----------
    uuid
        UUID to check.
    """
    try:
        user = models.User.objects.get(uuid=uuid)
    except models.User.DoesNotExist:
        return None

    if isinstance(user, models.User):
        return user

    return None