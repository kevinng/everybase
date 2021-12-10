import uuid
from django.db import models

from common.models import Standard
from files import models as fimods

class Lead(Standard):
    """Lead.

    Last updated: 12 November 2021, 7:59 PM
    """
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    author = models.ForeignKey(
        'relationships.User',
        related_name='users_who_authored_this_lead',
        related_query_name='users_who_authored_this_lead',
        on_delete=models.PROTECT,
        db_index=True
    )
    lead_type = models.CharField(
        max_length=20,
        choices=[
            ('buying', 'Buying'),
            ('selling', 'Selling')
        ],
        db_index=True
    )
    author_type = models.CharField(
        max_length=20,
        choices=[
            ('direct', 'Direct'),
            ('broker', 'Broker')
        ],
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200)
    details = models.TextField()
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='lead_with_this_country',
        related_query_name='lead_with_this_country',
        null=True,
        blank=True,
        db_index=True
    )
    commission_pct = models.FloatField(
        db_index=True,
        null=True,
        blank=True
    )
    commission_payable_by = models.CharField(
        max_length=20,
        choices=[
            ('me', 'Me'),
            ('buyer', 'Buyer'),
            ('seller', 'Seller')
        ],
        null=True,
        blank=True
    )
    commission_payable_after = models.CharField(
        max_length=50,
        choices=[
            ('initial_deposit_received', 'Initial deposit received'),
            ('goods_shipped', 'Goods shipped'),
            ('buyer_received_goods_services', 'Buyer received goods/services'),
            ('full_payment_received', 'Full payment received'),
            ('others', 'others')
        ],
        null=True,
        blank=True
    )
    commission_payable_after_others = models.TextField(
        null=True,
        blank=True
    )
    other_commission_details = models.TextField(
        null=True,
        blank=True
    )
    internal_notes = models.TextField(
        null=True,
        blank=True
    )
    onboarding = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    onboarded = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    def images(self):
        return fimods.File.objects.filter(
            lead=self.id,
            file_type__icontains='image'
        )

    def documents(self):
        return fimods.File.objects.filter(
            lead=self.id,
            file_type__icontains='pdf'
        )

    def image_count(self):
        return fimods.File.objects.filter(
            lead=self.id,
            file_type__icontains='image'
        ).count()

    def document_count(self):
        return fimods.File.objects.filter(
            lead=self.id,
            file_type__icontains='pdf'
        ).count()

class SavedLead(Standard):
    """Saved lead.

    Last updated: 15 October 2021, 11:56 PM
    """
    saved = models.DateTimeField(
        db_index=True
    )

    saver = models.ForeignKey(
        'relationships.User',
        related_name='user_with_this_saved_leads',
        related_query_name='user_with_this_saved_leads',
        on_delete=models.PROTECT,
        db_index=True        
    )
    lead = models.ForeignKey(
        'Lead',
        related_name='lead_with_this_saved_leads',
        related_query_name='lead_with_this_saved_leads',
        on_delete=models.PROTECT,
        db_index=True  
    )

    class Meta:
        unique_together = ('lead', 'saver')

class LeadDetailAccess(Standard):
    """Records access to a lead's detail by an accessor user

    Last updated: 27 October 2021, 8:46 PM
    """
    lead = models.ForeignKey(
        'Lead',
        related_name='detail_accesses_with_this_lead',
        related_query_name='detail_accesses_with_this_lead',
        on_delete=models.PROTECT,
        db_index=True        
    )
    accessor = models.ForeignKey(
        'relationships.User',
        related_name='detail_accesses_with_this_accessor',
        related_query_name='detail_accesses_with_this_accessor',
        on_delete=models.PROTECT,
        db_index=True  
    )

    access_count = models.IntegerField(
        db_index=True
    )

    class Meta:
        unique_together = ('lead', 'accessor')

class ContactRequest(Standard):
    """A contact request. Note: contactor may or may not already be connected
    with the lead author.

    Last updated: 15 November 2021, 4:53 PM
    """
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    response = models.CharField(
        max_length=20,
        choices=[
            ('accept', 'Accept'),
            ('reject', 'Reject')
        ],
        null=True,
        blank=True,
        db_index=True
    )

    contactor = models.ForeignKey(
        'relationships.User',
        related_name='contact_requests_with_this_contactor',
        related_query_name='contact_requests_with_this_contactor',
        on_delete=models.PROTECT,
        db_index=True
    )
    lead = models.ForeignKey(
        'Lead',
        related_name='contact_requests_with_this_lead',
        related_query_name='contact_requests_with_this_lead',
        on_delete=models.PROTECT,
        db_index=True
    )
    message = models.TextField()

    class Meta:
        unique_together = ('contactor', 'lead')

class FilterFormPost(Standard):
    """Filter form post by a user.

    Last updated: 7 December 2021, 8:06 PM
    """
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    details = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    is_buying = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_selling = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_direct = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_agent = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

    user_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    lead_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    is_initial_deposit = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_goods_shipped = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_payment_received = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_goods_received = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_others = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        'relationships.User',
        related_name='filter_form_posts',
        related_query_name='filter_form_posts',
        on_delete=models.PROTECT,
        db_index=True,
        null=True,
        blank=True
    )

class WhatsAppLeadAuthorClick(Standard):
    lead = models.ForeignKey(
        'Lead',
        related_name='whatsapp_lead_author_clicks',
        related_query_name='whatsapp_lead_author_clicks',
        on_delete=models.PROTECT,
        db_index=True
    )
    contactor = models.ForeignKey(
        'relationships.User',
        related_name='whatsapp_lead_author_clicks',
        related_query_name='whatsapp_lead_author_clicks',
        on_delete=models.PROTECT,
        db_index=True
    )
    access_count = models.IntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        unique_together = ('lead', 'contactor')