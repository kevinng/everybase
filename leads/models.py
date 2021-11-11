import uuid
from django.db import models
from common.models import Standard

class Lead(Standard):
    """Lead.

    Last updated: 27 October 2021, 8:46 PM
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
    country_string = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
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
    """Contact request.

    Last updated: 27 October 2021, 8:46 PM
    """
    requested = models.DateTimeField(db_index=True)
    responded = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
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

    requester = models.ForeignKey(
        'relationships.User',
        related_name='contact_requests_with_this_requester',
        related_query_name='contact_requests_with_this_requester',
        on_delete=models.PROTECT,
        db_index=True
    )
    requestee = models.ForeignKey(
        'relationships.User',
        related_name='contact_requests_with_this_requestee',
        related_query_name='contact_requests_with_this_requestee',
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
    access_count = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )