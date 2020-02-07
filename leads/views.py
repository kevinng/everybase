from django.views.generic import CreateView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect

from .models import LeadModelForm
from common.tasks import send_email
from everybase.settings import LEAD_SIGN_UP_NOTIFICATION_LIST

class LeadCaptureView(CreateView):
    form_class = LeadModelForm
    template_name = 'leads/index.html'

    def post(self, request):
        form = LeadModelForm(request.POST)
        if form.is_valid():
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                form.instance.ip_address = x_forwarded_for.split(',')[-1]
            else:
                form.instance.ip_address = request.META.get('REMOTE_ADDR')
            lead = form.save()
            lead.save()

            # Notify Everybase staff member
            i = form.instance
            context = {
                'name': i.name,
                'email': i.email,
                'ip_address': i.ip_address,
                'chat_app': i.chat_app,
                'whatsapp_no': i.whatsapp_no,
                'wechat_no': i.wechat_no,
                'i_want_to': i.i_want_to,
                'i_am_interested_to_buy': i.i_am_interested_to_buy,
                'created': i.created
            }
            template = lambda template: 'leads/email/' + template
            send_email.delay(
                render_to_string(template('new_lead_notification_subject.txt'), {}),
                render_to_string(template('new_lead_notification.html'), context),
                'system@everybase.co',
                LEAD_SIGN_UP_NOTIFICATION_LIST,
                html_message=render_to_string(template('new_lead_notification.html'), context)
            )

            return render(request, 'leads/done.html')

        return render(request, self.template_name, {'form': form})