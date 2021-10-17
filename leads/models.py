from django.db import models
from common.models import Standard

class Lead(Standard):
    """Lead.

    Last updated: 15 October 2021, 12:02 PM
    """
    closed = models.DateTimeField(
        db_index=True
    )
    owner = models.ForeignKey(
        'relationships.User',
        related_name='users_who_own_this_lead',
        related_query_name='users_who_own_this_lead',
        on_delete=models.PROTECT,
        db_index=True
    )
    lead_type = models.CharField(
        max_length=20,
        choices=[
            ('direct', 'Direct'),
            ('broker', 'Broker')
        ],
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_buying = models.BooleanField(
        db_index=True
    )
    agent_sale_commission_pct = models.FloatField(db_index=True)
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='lead_with_this_country',
        related_query_name='lead_with_this_country',
        null=True,
        blank=True,
        db_index=True
    )
    tags = models.ManyToManyField(
        'LeadTag',
        related_name='lead_with_this_tags',
        related_query_name='lead_with_this_tags',
        db_index=True        
    )

class LeadDocument(Standard):
    """Document associated with a lead.
    
    Last updated: 15 October 2021, 11:56 PM
    """
    uploaded = models.DateTimeField(
        db_index=True
    )
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
    
    Last updated: 15 October 2021, 11:56 PM
    """
    uploaded = models.DateTimeField(
        db_index=True
    )
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

class LeadTag(Standard):
    """File associated with a lead.
    
    Last updated: 15 October 2021, 11:56 PM
    """
    tag = models.CharField(
        max_length=200,
        db_index=True
    )
    internal_notes = models.TextField(
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