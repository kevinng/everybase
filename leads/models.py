from operator import mod
import uuid
from django.db import models
from common.models import Standard

class Lead(Standard):
    """Lead.

    Last updated: 24 February 2022, 5:06 AM
    """
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    author = models.ForeignKey(
        'relationships.User',
        related_name='leads_author',
        related_query_name='leads_author',
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
        default='direct',
        choices=[
            ('direct', 'Direct'),
            ('broker', 'Broker') # Middleman
        ],
        db_index=True
    )
    buy_country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='leads_buy_country',
        related_query_name='leads_buy_country',
        null=True,
        blank=True,
        db_index=True
    )
    sell_country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='leads_sell_country',
        related_query_name='leads_sell_country',
        null=True,
        blank=True,
        db_index=True
    )
    details = models.TextField()
    need_agent = models.BooleanField(
        db_index=True
    )
    commission_payable_by = models.CharField(
        max_length=20,
        choices=[
            ('me', 'Me'),
            ('buyer', 'Buyer'),
            ('seller', 'Seller')
        ],
        null=True,
        blank=True,
        db_index=True
    )
    commission_type = models.CharField(
        max_length=20,
        choices=[
            ('percentage', 'Percentage'),
            ('other', 'Other')
        ],
        null=True,
        blank=True,
        db_index=True
    )
    commission_type_other = models.TextField(
        null=True,
        blank=True
    )
    is_comm_negotiable = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    commission = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    avg_deal_size = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    commission_payable_after = models.CharField(
        max_length=50,
        choices=[
            ('initial_deposit_received', 'Initial deposit received'),
            ('goods_shipped', 'Goods shipped'),
            ('buyer_received_goods_services', 'Buyer received goods/services'),
            ('full_payment_received', 'Full payment received'),
            ('other', 'Other')
        ],
        null=True,
        blank=True,
        db_index=True
    )
    commission_payable_after_other = models.TextField(
        null=True,
        blank=True
    )
    other_agent_details = models.TextField(
        null=True,
        blank=True
    )
    need_logistics_agent = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    other_logistics_agent_details = models.TextField(
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

    saved_count = models.IntegerField(
        default=0,
        db_index=True
    )
    search_appearance_count = models.IntegerField(
        default=1, # Prevent division by 0
        db_index=True
    )
    search_to_lead_details_count = models.IntegerField(
        default=0,
        db_index=True
    )
    search_to_user_details_count = models.IntegerField(
        default=0,
        db_index=True
    )

    # Keep for data
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    # Keep for future
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='leads_country',
        related_query_name='leads_country',
        null=True,
        blank=True,
        db_index=True
    )

    def avg_deal_comm(self):
        return self.commission / 100 * self.avg_deal_size

class LeadDetailView(Standard):
    """Lead detail view.

    Last updated: 11 February 2022, 10:11 PM
    """
    viewer = models.ForeignKey(
        'relationships.User',
        related_name='lead_detail_views',
        related_query_name='lead_detail_views',
        on_delete=models.PROTECT,
        db_index=True  
    )
    lead = models.ForeignKey(
        'Lead',
        related_name='lead_detail_views',
        related_query_name='lead_detail_views',
        on_delete=models.PROTECT,
        db_index=True        
    )

    count = models.IntegerField(
        db_index=True
    )

    class Meta:
        unique_together = ('viewer', 'lead')

class WhatsAppClick(Standard):
    """User's click on to WhatsApp button

    Last updated: 11 February 2022, 10:15 PM
    """
    contactee = models.ForeignKey(
        'relationships.User',
        related_name='whatsapp_clicks_contactee',
        related_query_name='whatsapp_clicks_contactee',
        on_delete=models.PROTECT,
        db_index=True
    )
    contactor = models.ForeignKey(
        'relationships.User',
        related_name='whatsapp_clicks_contactor',
        related_query_name='whatsapp_clicks_contactor',
        on_delete=models.PROTECT,
        db_index=True
    )
    count = models.IntegerField(default=0)

class WhatsAppMessageBody(Standard):
    """Message body when a user contacts another user

    Last updated: 28 January 2022, 6:26 PM
    """
    contactee = models.ForeignKey(
        'relationships.User',
        related_name='whatsapp_message_bodies_contactee',
        related_query_name='whatsapp_message_bodies_contactee',
        on_delete=models.PROTECT,
        db_index=True
    )
    contactor = models.ForeignKey(
        'relationships.User',
        related_name='whatsapp_message_bodies_contactor',
        related_query_name='whatsapp_message_bodies_contactor',
        on_delete=models.PROTECT,
        db_index=True
    )
    body = models.TextField()

class AgentQuery(Standard):
    """Agent query

    Last updated: 11 February 2022, 9:56 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='agent_query',
        related_query_name='agent_query',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    search = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        'common.Country',
        related_name='agent_queries',
        related_query_name='agent_queries',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    sort_by = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_index=True
    )

class LeadQuery(Standard):
    """Lead query

    Last updated: 24 February 2022, 6:00 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='lead_query',
        related_query_name='lead_query',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    search = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    wants_to = models.CharField(
        max_length=20,
        choices=[
            ('buy_or_sell', 'Buy or Sell'),
            ('buy', 'Buy'),
            ('sell', 'Sell')
        ],
        db_index=True
    )
    sort_by = models.CharField(
        max_length=20,
        choices=[
            ('relevance', 'Relevance'),
            ('comm_percent_hi_lo', 'Avg Comm % High to Low'),
            ('comm_percent_lo_hi', 'Avg Comm % Low to High'),
            ('comm_dollar_hi_lo', 'Avg Comm $ High to Low'),
            ('comm_dollar_lo_hi', 'Avg Comm $ Low to High')
        ],
        null=True,
        blank=True,
        db_index=True
    )
    buy_country = models.ForeignKey(
        'common.Country',
        related_name='lead_queries_buy_country',
        related_query_name='lead_queries_buy_country',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    sell_country = models.ForeignKey(
        'common.Country',
        related_name='lead_queries_sell_country',
        related_query_name='lead_queries_sell_country',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

# Not in use, keep for data
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

# Not in use, keep for data
class WhatsAppLeadAuthorClick(Standard):
    """User's click on to WhatsApp lead author
    
    Last updated: 28 January 2022, 6:26 PM
    """
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
    count = models.IntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        unique_together = ('lead', 'contactor')

# Not in use, keep for future implementation
class SavedLead(Standard):
    """Saved lead.

    Last updated: 15 October 2021, 11:56 PM
    """
    saved = models.DateTimeField(
        db_index=True
    )

    saver = models.ForeignKey(
        'relationships.User',
        related_name='saved_leads_saver',
        related_query_name='saved_leads_saver',
        on_delete=models.PROTECT,
        db_index=True        
    )
    lead = models.ForeignKey(
        'Lead',
        related_name='saved_leads_lead',
        related_query_name='saved_leads_lead',
        on_delete=models.PROTECT,
        db_index=True  
    )

    class Meta:
        unique_together = ('lead', 'saver')