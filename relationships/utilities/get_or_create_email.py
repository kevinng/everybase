from typing import Union
from django.core.validators import validate_email
from relationships import models as relmods

def get_or_create_email(
        email: str
    ) -> Union[relmods.Email, bool]:
    """Returns email object reference created/got, or False if error.

    Parameters
    ----------
    email
        Raw email to get or create.
    """
    try:
        validate_email(email)
    except Exception:
        return None

    email, _ = relmods.Email.objects.get_or_create(email=email)

    return email