from urllib.parse import urljoin
from django.urls import reverse
from everybase import settings
from chat.constants import intents, messages
from chat.tests.library import ChatTest
from chat.tasks._archive.send_contact_request_confirm import send_contact_request_confirm
from chat.tasks._archive.send_contact_request_exchanged_author import \
    send_contact_request_exchanged_author
from chat.tasks._archive.send_contact_request_exchanged_contactor import \
    send_contact_request_exchanged_contactor
from relationships import models as relmods
from relationships.utilities._archive.get_create_whatsapp_link import \
    get_create_whatsapp_link
from leads import models as lemods

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
        self.contactor = self.user_2
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
            message='Hi, please connect to discuss opportunities.'
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

class ContactRequestExchangedAuthorTest(ChatTest):
    fixtures = [
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20211126__relationships__user',
        'setup/common__country__stagingdevelopment'
    ]
    
    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send(self):
        self.contactor_ph = relmods.PhoneNumber.objects.create(
            country_code='54321',
            national_number='0987654321'
        )
        self.contactor = self.user_2
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
            message='Hi, please connect to discuss opportunities.'
        )
        
        msg = send_contact_request_exchanged_author(
            self.contact_request.id,
            True
        )

        self.assert_context_body(
            intents.CONTACT_REQUEST,
            messages.CONTACT_REQUEST__EXCHANGED_AUTHOR,
            msg.body, {
                'contactor_first_name': self.contactor.first_name,
                'contactor_last_name': self.contactor.last_name,
                'contactor_country': self.contactor.country.name,
                'message': self.contact_request.message,
                'lead_type': self.lead.lead_type,
                'lead_title': self.lead.title,
                'lead_detail_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads:detail', args=[self.lead.uuid])),
                'whatsapp_url': get_create_whatsapp_link(
                    self.lead.author, self.contactor),
                'contact_request_detail_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads__root:contact_request_detail',
                    args=[self.contact_request.uuid])),
                'contact_request_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads__root:contact_request_list')
                ),
                'create_lead_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads:create')
                )
            }
        )

class ContactRequestExchangedContactorTest(ChatTest):
    fixtures = [
        'setup/20210527__relationships__phonenumber',
        'setup/20210527__relationships__phonenumbertype',
        'setup/20211126__relationships__user',
        'setup/common__country__stagingdevelopment'
    ]
    
    def setUp(self):
        super().setUp(intents.NO_INTENT, messages.NO_MESSAGE)

    def test_send(self):
        self.contactor_ph = relmods.PhoneNumber.objects.create(
            country_code='54321',
            national_number='0987654321'
        )
        self.contactor = self.user_2
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
            message='Hi, please connect to discuss opportunities.'
        )

        msg = send_contact_request_exchanged_contactor(
            self.contact_request.id,
            True
        )
        
        self.assert_context_body(
            intents.CONTACT_REQUEST,
            messages.CONTACT_REQUEST__EXCHANGED_CONTACTOR,
            msg.body, {
                'author_first_name': self.lead.author.first_name,
                'author_last_name': self.lead.author.last_name,
                'author_country': self.lead.author.country.name,
                'lead_type': self.lead.lead_type,
                'lead_title': self.lead.title,
                'lead_detail_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads:detail', args=[self.lead.uuid])),
                'whatsapp_url': get_create_whatsapp_link(
                    self.contactor, self.lead.author),
                'contact_request_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads__root:contact_request_list')
                ),
                'create_lead_url': urljoin(
                    settings.BASE_URL,
                    reverse('leads:create')
                )
            }
        )