from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from relationships import models

def email_exists(email: str) -> bool:
    """Returns User model reference if an existing user owns this email, False otherwise. Returns None if error."""
    if email is None or email.strip() == '':
        return None

    try:
        validate_email(email)
    except ValidationError as e:
        return None

    try:
        e = models.Email.objects.get(email=email)
        u = models.User.objects.filter(
            email=e.id, # User has email
            registered__isnull=False, # User is registered
            django_user__isnull=False, # User has a Django user linked
            deleted__isnull=True, # User is not deleted
        ).first()

        if u is not None:
            # Email belongs to an existing user
            return u
    except models.Email.DoesNotExist:
        return False

    return False