from django.db import models
from common.models import Standard

class Lead(Standard):
    """Lead.

    Last updated: 24 September 2021, 10:48 PM
    """
    closed = models.DateTimeField(db_index=True)
    is_buying = models.BooleanField(db_index=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    agent_sale_commission_pct = models.FloatField(db_index=True)
    location = models.CharField(max_length=200)


    owner_role = models.TextField(
        max_length=200,
        choices=[
            ('broker', 'Broker'),
            ('direct', 'Direct')
        ]
    )

class LeadFile(Standard):
    """File associated with a lead.

    Last updated: 24 September 2021, 10:48 PM
    """
    title = models.CharField(max_length=200)
    file_type = models.CharField(
        max_length=200,
        choices=[
            ('document', 'Document'),
            ('image', 'Image')
        ]
    )

    file = models.ForeignKey(
        'files.File',
        related_name='lead_files',
        related_query_name='lead_files',
        on_delete=models.PROTECT,
        db_index=True
    )
    lead = models.ForeignKey(
        'Lead',
        related_name='lead_files',
        related_query_name='lead_files',
        on_delete=models.PROTECT,
        db_index=True
    )

class SavedLead(Standard):
    """Saved lead.

    Last updated: 24 September 2021, 10:48 PM
    """

    lead = models.ForeignKey(
        'Lead',
        related_name='saved_leads',
        related_query_name='saved_leads',
        on_delete=models.PROTECT,
        db_index=True
    )