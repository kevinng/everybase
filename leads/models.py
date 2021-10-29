from django.db import models
from common.models import Standard
from hashid_field import HashidAutoField

class Lead(Standard):
    """Lead.

    Last updated: 27 October 2021, 8:46 PM
    """
    author = models.ForeignKey(
        'relationships.User',
        related_name='users_who_authored_this_lead',
        related_query_name='users_who_authored_this_lead',
        on_delete=models.PROTECT,
        db_index=True
    )
    is_buying = models.BooleanField(db_index=True)
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
    commission_payable_after = models.CharField(
        max_length=50,
        choices=[
            ('initial_deposit_received', 'Initial deposit received'),
            ('goods_shipped', 'Goods shipped'),
            ('buyer_received_goods_services', 'Buyer received goods/services'),
            ('full_payment_received', 'Full payment received')
        ],
        null=True,
        blank=True
    )
    other_commission_details = models.TextField(
        null=True,
        blank=True
    )

class LeadDocument(Standard):
    """Document associated with a lead.
    
    Last updated: 27 October 2021, 8:46 PM
    """
    id = HashidAutoField(primary_key=True)
    lead = models.ForeignKey(
        'Lead',
        related_name='users_who_own_this_lead_document',
        related_query_name='users_who_own_this_lead_document',
        on_delete=models.PROTECT,
        db_index=True
    )
    file = models.ForeignKey(
        'files.File',
        related_name='leads_with_this_document',
        related_query_name='leads_with_this_document',
        on_delete=models.PROTECT,
        db_index=True
    )

class LeadImage(Standard):
    """Document associated with a lead.
    
    Last updated: 27 October 2021, 8:46 PM
    """
    id = HashidAutoField(primary_key=True)
    lead = models.ForeignKey(
        'Lead',
        related_name='users_who_own_this_lead_image',
        related_query_name='users_who_own_this_lead_image',
        on_delete=models.PROTECT,
        db_index=True
    )
    file = models.ForeignKey(
        'files.File',
        related_name='leads_with_this_image',
        related_query_name='leads_with_this_image',
        on_delete=models.PROTECT,
        db_index=True
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

class LeadDocumentAccess(Standard):
    """Lead document access

    Last updated: 27 October 2021, 8:46 PM
    """
    lead_document = models.ForeignKey(
        'LeadDocument',
        related_name='document_accesses_with_this_lead',
        related_query_name='document_accesses_with_this_lead',
        on_delete=models.PROTECT,
        db_index=True        
    )
    accessor = models.ForeignKey(
        'relationships.User',
        related_name='document_accesses_with_this_lead',
        related_query_name='document_accesses_with_this_lead',
        on_delete=models.PROTECT,
        db_index=True  
    )

    access_count = models.IntegerField(
        db_index=True
    )

    class Meta:
        unique_together = ('lead_document', 'accessor')

class LeadImageAccess(Standard):
    """Lead image access

    Last updated: 27 October 2021, 8:46 PM
    """
    lead_image = models.ForeignKey(
        'LeadDocument',
        related_name='image_accesses_with_this_lead',
        related_query_name='image_accesses_with_this_lead',
        on_delete=models.PROTECT,
        db_index=True        
    )
    accessor = models.ForeignKey(
        'relationships.User',
        related_name='image_accesses_with_this_lead',
        related_query_name='image_accesses_with_this_lead',
        on_delete=models.PROTECT,
        db_index=True  
    )

    access_count = models.IntegerField(
        db_index=True
    )

    class Meta:
        unique_together = ('lead_document', 'accessor')