from relationships import models
from chat import models as cmods
from files import models as fimods

def run():
    users = models.User.objects.filter(id__gt=3)

    for u in users:
        for tim in cmods.TwilioInboundMessage.objects.filter(from_user=u):
            cmods.TwilioInboundMessageLogEntry.objects.filter(message=tim).delete()
            tim.delete()

        for tim in cmods.TwilioInboundMessage.objects.filter(to_user=u):
            cmods.TwilioInboundMessageLogEntry.objects.filter(message=tim).delete()
            tim.delete()

        fimods.File.objects.filter(uploader=u).delete()

        for tom in cmods.TwilioOutboundMessage.objects.filter(from_user=u):
            cmods.TwilioInboundMessage.objects.filter(twilml_response_to=tom).delete()
            tom.delete()

        for tom in cmods.TwilioOutboundMessage.objects.filter(to_user=u):
            cmods.TwilioInboundMessage.objects.filter(twilml_response_to=tom).delete()
            tom.delete()

        u.delete()