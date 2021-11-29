from urllib.parse import urljoin
from django.urls import reverse
from everybase import settings
from chat.constants import intents, messages
from chat.tests.library import ChatTest
from chat.tasks.send_contact_request_confirm import send_contact_request_confirm
from relationships import models as relmods
from leads import models as lemods
from common import models as commods

class ContactRequestConfirmTest(ChatTest):
    fixtures = [
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20211126__relationships__user',
        'setup/common__country__stagingdevelopment'
    ]
    
    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send(self):
        self.country = commods.Country.objects.get(pk=511) # Australia
        self.contactor = relmods.User.objects.create(
            first_name='Kevin2',
            last_name='Ng2',
            country=self.country
        )
        self.lead = lemods.Lead.objects.create(
            author=self.user,
            lead_type='buying',
            author_type='direct',
            title='Cocoa for Sale',
            details='Good for hot chocolate.'
        )
        self.contact_request = lemods.ContactRequest.objects.create(
            contactor=self.contactor,
            lead=self.lead,
            message='Hi, place connect to discuss opportunities.'
        )
        
        msg = send_contact_request_confirm(
            self.contact_request.id,
            True
        )

        self.assert_context_body(
            intents.CONTACT_REQUEST,
            messages.CONTACT_REQUEST__CONFIRM,
            msg.body, {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'message': self.contact_request.message,
                'contactor_first_name': self.contactor.first_name,
                'contactor_last_name': self.contactor.last_name,
                'contactor_country': self.contactor.country.name,
                'lead_type': self.lead.lead_type,
                'lead_title': self.lead.title,
                'lead_detail_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads:detail', args=[self.lead.uuid])),
                'contact_request_detail_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads__root:contact_request_detail',
                    args=[self.contact_request.uuid]))
            }
        )

    def tearDown(self):
        self.contact_request.delete()
        self.contactor.delete()
        self.lead.delete()
        return super().tearDown()

class ContactRequestExchangedAuthorTest(ChatTest):
    # fixtures = [
    #     'setup/20210527__relationships__phonenumber',
    #     'setup/20210527__relationships__phonenumbertype',
    #     'setup/20211126__relationships__user',
    #     ''
    # ]
    
    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send(self):
        pass
        # msg = send_login_confirm(self.user.id, True)
        # self.assert_context_body(
        #     intents.LOGIN,
        #     messages.LOGIN__CONFIRM,
        #     msg.body, {
        #         'first_name': self.user.first_name,
        #         'last_name': self.user.last_name
        #     }
        # )


class ContactRequestExchangedContactorTest(ChatTest):
    fixtures = [
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20211126__relationships__user'
    ]
    
    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send(self):
        pass
        # msg = send_login_confirm(self.user.id, True)
        # self.assert_context_body(
        #     intents.LOGIN,
        #     messages.LOGIN__CONFIRM,
        #     msg.body, {
        #         'first_name': self.user.first_name,
        #         'last_name': self.user.last_name
        #     }
        # )