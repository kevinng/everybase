from relationships import models as relmods

def setup_user_phone_number(
        name: str = 'Kevin Ng',
        country_code: str = '12345',
        national_number: str = '1234567890'
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
    """
    phone_number = relmods.PhoneNumber.objects.create(
        country_code=country_code,
        national_number=national_number)

    user = relmods.User.objects.create(
        phone_number=phone_number,
        name=name)

    return (user, phone_number)