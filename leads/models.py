import uuid as uuidlib
from django.db import models
import files.models as fimods
from common.models import Standard
from django.utils.text import slugify
    
class Lead(Standard):
    """Lead.

    Last updated: 12 May 2022, 2:35 PM
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuidlib.uuid4,
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
    headline = models.CharField(
        max_length=80,
        db_index=True
    )
    commission_type = models.CharField(
        max_length=20,
        choices=[
            ('earning', 'Earning'),
            ('percentage', 'Percentage'),
            ('other', 'Other')
        ],
        db_index=True
    )
    min_commission_percentage = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    max_commission_percentage = models.FloatField(
        null=True,
        blank=True,
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
    questions = models.TextField(
        null=True,
        blank=True
    )
    
    slug_link = models.CharField(
        max_length=200,
        unique=True,
        db_index=True
    )
    slug_tokens = models.TextField(
        null=True,
        blank=True
    )

    internal_notes = models.TextField(
        null=True,
        blank=True
    )

    # Not in use

    currency = models.ForeignKey(
        'payments.Currency',
        on_delete=models.PROTECT,
        related_name='leads_currency',
        related_query_name='leads_currency',
        db_index=True,
        null=True,
        blank=True
    )
    author_type = models.CharField(
        max_length=20,
        default='direct',
        choices=[
            ('direct', 'Direct'),
            ('broker', 'Broker') # Middleman
        ],
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='leads_country',
        related_query_name='leads_country',
        null=True,
        blank=True,
        db_index=True
    )
    agent_job = models.TextField(
        null=True,
        blank=True
    )
    is_promoted = models.BooleanField(
        blank=True,
        null=True,
        db_index=True
    )
    
    commission_earnings = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    commission_quantity_unit_string = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    commission_type_other = models.TextField(
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
    other_comm_details = models.TextField(
        null=True,
        blank=True
    )
    comm_details = models.TextField(
        null=True,
        blank=True
    )

    is_comm_negotiable = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

    question_1 = models.TextField(
        blank=True,
        null=True
    )
    question_2 = models.TextField(
        blank=True,
        null=True
    )
    question_3 = models.TextField(
        blank=True,
        null=True
    )

    impressions = models.IntegerField(
        default=1, # Prevent division by 0
        db_index=True
    )
    clicks = models.IntegerField(
        default=0,
        db_index=True
    )

    title = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    avg_deal_size = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    need_agent = models.BooleanField(
        db_index=True,
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

    def __str__(self):
        s = self.headline
        if self.min_commission_percentage is not None and self.max_commission_percentage is not None:
            s += f', {self.min_commission_percentage}% to {self.max_commission_percentage}'
        if self.lead_type == 'selling':
            s += f', {self.lead_type}, from {self.buy_country.name}'
        if self.lead_type == 'buying':
            s += f', {self.lead_type}, to {self.sell_country.name}'

        s += f' [{self.id}]'

        return s
    
    def refresh_slug(self):
        first_lead = Lead.objects.all().order_by('-id').first()
        if first_lead is None:
            this_id = 0
        elif self.id is None:
            # Compute ID because it's not been set.
            # Race condition and collison possible but very unlikely.
            this_id = Lead.objects.all().order_by('-id').first().id + 1
        else:
            this_id = self.id

        self.slug_tokens = f'{self.headline} {this_id}'
        self.slug_link = slugify(self.slug_tokens)

    def save(self, *args, **kwargs):
        self.refresh_slug()
        return super().save(*args, **kwargs)

    def cover_photo(self):
        """Returns cover photo"""
        return fimods.File.objects\
            .filter(lead=self, deleted__isnull=True)\
            .order_by('-created')\
            .first()

    def num_applications(self):
        """Number of applications on this lead"""
        return Application.objects.filter(
            lead=self,
            deleted__isnull=True
        ).count()

    def display_images(self):
        """Returns display images."""
        NUM_DISPLAY_IMAGES = 1

        return fimods.File.objects\
            .filter(lead=self, deleted__isnull=True)\
            .order_by('-created')[:NUM_DISPLAY_IMAGES]

    # def num_images(self):
    #     """Returns the number of display images for this lead"""
    #     return fimods.File.objects\
    #         .filter(lead=self, deleted__isnull=True)\
    #         .order_by('-created')[:3].count()

    # def num_comments(self):
    #     """Number of comments on this lead"""
    #     return LeadComment.objects.filter(
    #         lead=self,
    #         deleted__isnull=True
    #     ).count()

    # def avg_deal_comm(self):
    #     return self.commission / 100 * self.avg_deal_size

    # def root_comments(self):
    #     """Returns root comments only (i.e., comments that are not replies to
    #     a comment. We do not chain replies and all replies are to root comments.
    #     """
    #     return LeadComment.objects.filter(
    #         lead=self,
    #         reply_to__isnull=True
    #     ).order_by('created')

    # def seo_title(self):
    #     """Returns SEO-optimized title"""
    #     lead_type = 'Buyer Importer' if self.lead_type == 'buying' else 'Seller Exporter'
    #     country = self.buy_country.name if self.lead_type == 'buying' else self.sell_country.name
    #     title = f'{ lead_type }, { country }'

    #     if self.slug_tokens is not None and len(self.slug_tokens.strip()) != 0:
    #         tokens = self.slug_tokens.split(',')
    #         tokens = [t.strip() for t in tokens]
    #         if len(tokens) > 0:
    #             keywords = tokens[0]
    #             for t in tokens[1:]:
    #                 if len(keywords) < 40:
    #                     keywords += ' ' + t
    #                 else:
    #                     break
                
    #             title += ' - ' + keywords

    #     return title

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
        default=0,
        db_index=True
    )

    class Meta:
        unique_together = ('viewer', 'lead')

class Application(Standard):
    """Agent application.

    Last updated: 5 May 2022, 12:36 PM
    """
    last_messaged = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    deleted_by = models.CharField(
        max_length=20,
        choices=[
            ('agent', 'Agent'),
            ('author', 'Author')
        ],
        null=True,
        blank=True,
        db_index=True
    )

    lead = models.ForeignKey(
        'Lead',
        related_name='applications',
        related_query_name='applications',
        on_delete=models.PROTECT,
        db_index=True
    )
    applicant = models.ForeignKey(
        'relationships.User',
        related_name='applications_as_applicant',
        related_query_name='applications_as_applicant',
        on_delete=models.PROTECT,
        db_index=True
    )

    has_experience = models.BooleanField(
        blank=True,
        null=True
    )
    has_buyers = models.BooleanField(
        blank=True,
        null=True
    )

    questions = models.TextField(
        blank=True,
        null=True
    )
    answers = models.TextField(
        blank=True,
        null=True
    )
    applicant_comments = models.TextField(
        blank=True,
        null=True
    )

    # Not in use

    question_1 = models.TextField(
        blank=True,
        null=True
    )
    answer_1 = models.TextField(
        blank=True,
        null=True
    )
    question_2 = models.TextField(
        blank=True,
        null=True
    )
    answer_2 = models.TextField(
        blank=True,
        null=True
    )
    question_3 = models.TextField(
        blank=True,
        null=True
    )
    answer_3 = models.TextField(
        blank=True,
        null=True
    )

    response = models.CharField(
        max_length=200,
        choices=[
            ('rejected', 'Rejected'),
            ('started_work', 'Started Work'),
            ('stopped_work', 'Stopped Work'),
        ],
        blank=True,
        null=True
    )

    def __str__(self):
        return f'({self.applicant}, {self.lead} [{self.id}])'

class ApplicationMessage(Standard):
    """Application message.

    Last updated: 7 April 2022, 10:06 PM
    """
    application = models.ForeignKey(
        'Application',
        related_name='messages',
        related_query_name='messages',
        on_delete=models.PROTECT,
        db_index=True
    )
    author = models.ForeignKey(
        'relationships.User',
        related_name='application_messages',
        related_query_name='application_messages',
        on_delete=models.PROTECT,
        db_index=True
    )

    body = models.TextField(
        blank=True,
        null=True
    )




























# Not in use


class LeadComment(Standard):
    """Comment on a lead

    Last updated: 14 February 2022, 11:33 AM
    """
    lead = models.ForeignKey(
        'Lead',
        related_name='lead_comments',
        related_query_name='lead_comments',
        on_delete=models.PROTECT,
        db_index=True
    )
    commentor = models.ForeignKey(
        'relationships.User',
        related_name='lead_comments_as_commentor',
        related_query_name='lead_comments_as_commentor',
        on_delete=models.PROTECT,
        db_index=True
    )

    body = models.TextField()

    reply_to = models.ForeignKey(
        'LeadComment',
        related_name='replies',
        related_query_name='replies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    def reply_comments(self):
        """Returns replies to this lead"""
        return LeadComment.objects.filter(
            reply_to=self,
            deleted__isnull=True
        ).order_by('created')

class LeadQuery(Standard):
    """Lead query.

    Last updated: 16 May 2022, 4:21 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='lead_query_logs',
        related_query_name='lead_query_logs',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    search = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    buy_sell = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    buy_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    sell_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    count = models.IntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        unique_together = ('user', 'search', 'buy_sell', 'buy_country', 'sell_country')

class ApplicationQueryLog(Standard):
    """Application query log.

    Last updated: 7 April 2022, 10:06 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='application_query_logs',
        related_query_name='application_query_logs',
        on_delete=models.PROTECT,
        db_index=True
    )

    status = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

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

class SavedLead(Standard):
    """Saved lead.

    Last updated: 28 February 2022, 10:32 PM
    """
    active = models.BooleanField(
        default=True,
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