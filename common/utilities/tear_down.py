from leads import models as lemods
from chat import models as chmods
from relationships import models as relmods
from common import models as commods

def tear_down():
    """Standard unit test database tear down procedures."""
    # Delete all models - order matters
    lemods.Lead.objects.all().delete()
    chmods.UserContext.objects.all().delete()
    chmods.TwilioInboundMessageMedia.objects.all().delete()
    chmods.TwilioOutboundMessage.objects.all().delete()
    chmods.TwilioInboundMessage.objects.all().delete()
    relmods.LoginToken.objects.all().delete()
    relmods.User.objects.all().delete()
    relmods.PhoneNumber.objects.all().delete()
    commods.Country.objects.all().delete()