from relationships import models
from chat import models as cmods
from files import models as fimods

def run():
    users = models.User.objects.filter(id__gt=3)

    for u in users:
        for tim in cmods.TwilioInboundMessage.objects.filter(from_user=u):
            tim.delete()

        for tim in cmods.TwilioInboundMessage.objects.filter(to_user=u):
            tim.delete()

        for f in fimods.File.objects.filter(uploader=u):
            f.delete()

        for tom in cmods.TwilioOutboundMessage.objects.filter(from_user=u):
            tom.delete()

        for tom in cmods.TwilioOutboundMessage.objects.filter(to_user=u):
            tom.delete()

        u.delete()