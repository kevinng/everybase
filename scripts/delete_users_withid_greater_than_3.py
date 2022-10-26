from relationships import models
from chat import models as cmods
from files import models as fimods

def run():
    users = models.User.objects.filter(id__gt=3)

    for u in users:
        for tim in cmods.TwilioInboundMessage.objects.filter(from_user=u):
            cmods.TwilioInboundMessageLogEntry.objects.filter(message=tim).delete()
            for tom in cmods.TwilioOutboundMessage.objects.filter(twilml_response_to=tim):
                for tsc in cmods.TwilioStatusCallback.objects.filter(message=tom):
                    cmods.TwilioStatusCallbackLogEntry.objects.filter(callback=tsc).delete()
                    tsc.delete()
                tom.delete()
            tim.delete()

        for tim in cmods.TwilioInboundMessage.objects.filter(to_user=u):
            cmods.TwilioInboundMessageLogEntry.objects.filter(message=tim).delete()
            for tom in cmods.TwilioOutboundMessage.objects.filter(twilml_response_to=tim):
                for tsc in cmods.TwilioStatusCallback.objects.filter(message=tom):
                    cmods.TwilioStatusCallbackLogEntry.objects.filter(callback=tsc).delete()
                    tsc.delete()
                tom.delete()

            tim.delete()

        fimods.File.objects.filter(uploader=u).delete()

        for tom in cmods.TwilioOutboundMessage.objects.filter(from_user=u):
            for tsc in cmods.TwilioStatusCallback.objects.filter(message=tom):
                cmods.TwilioStatusCallbackLogEntry.objects.filter(callback=tsc).delete()
                tsc.delete()
            tom.delete()

        for tom in cmods.TwilioOutboundMessage.objects.filter(to_user=u):
            for tsc in cmods.TwilioStatusCallback.objects.filter(message=tom):
                cmods.TwilioStatusCallbackLogEntry.objects.filter(callback=tsc).delete()
                tsc.delete()
            tom.delete()

        models.UserAgent.objects.filter(user=u).delete()

        u.delete()