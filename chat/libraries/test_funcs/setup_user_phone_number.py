import pytz, datetime
from relationships import models as relmods
from everybase.settings import TIME_ZONE

def setup_user_phone_number(
        name: str = 'Kevin Ng',
        country_code: str = '12345',
        national_number: str = '1234567890',
        registered: bool = False
    ):
    """Create user and phone number

    Parameters
    ----------
    name
        User's name
    country_code
        Country code of the user's phone number
    national_number
        National number of the user's phone number
    registered
        True if user has registered
    """
    phone_number = relmods.PhoneNumber.objects.create(
        country_code=country_code,
        national_number=national_number)

    user = relmods.User.objects.create(
        phone_number=phone_number,
        name=name)

    if registered:
        sgtz = pytz.timezone(TIME_ZONE)
        user.registered = datetime.datetime.now(tz=sgtz)
        user.save()

    return (user, phone_number)