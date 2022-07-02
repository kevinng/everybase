import uuid as uuidlib
from urllib.parse import urljoin

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify

from everybase import settings

from common.models import Standard, Choice
    
class Lead(Standard):
    """Lead.

    Last updated: 2 July 2022, 12:24 PM
    """
    uuid = models.UUIDField(
        unique=True,
        default=uuidlib.uuid4,
        editable=False,
        db_index=True
    )

    author = models.ForeignKey(
        'relationships.User',
        related_name='leads_with_author',
        related_query_name='leads_with_author',
        on_delete=models.PROTECT,
        db_index=True
    )
    lead_type = models.CharField(
        max_length=20,
        choices=[
            ('buying', 'Buying'),
            ('selling', 'Selling'),
            ('need_logistics', 'Logistics'),
            ('sourcing_agent', 'Sourcing Agent'),
            ('sales_agent', 'Sales Agent'),
            ('logistics_agent', 'Logistics Agent'),
            ('other', 'Other')
        ],
        db_index=True
    )

    body = models.TextField(
        blank=True,
        null=True
    )

    has_insights = models.BooleanField(
        null=True,
        blank=True
    )
    internal_notes = models.TextField(
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

    # Not in use

    category = models.ForeignKey(
        'LeadCategory',
        related_name='leads',
        related_query_name='leads',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        db_index=True
    )

    headline = models.CharField(
        max_length=80,
        db_index=True
    )
    details = models.TextField(
        null=True,
        blank=True
    )

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
    agent_job = models.TextField(
        null=True,
        blank=True
    )
    is_promoted = models.BooleanField(
        blank=True,
        null=True,
        db_index=True
    )
    
    commission_type = models.CharField(
        max_length=20,
        choices=[
            ('negotiable', 'Negotiable'),
            ('earning', 'Earning'),
            ('percentage', 'Percentage'),
            ('usd_mt', 'USD per MT'),
            ('other', 'Other')
        ],
        db_index=True
    )
    comm_details = models.TextField(
        null=True,
        blank=True
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
    is_comm_negotiable = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    commission_usd_mt = models.FloatField(
        null=True,
        blank=True,
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
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='leads_country',
        related_query_name='leads_country',
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
    questions = models.TextField(
        null=True,
        blank=True
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

        s += f', {self.lead_type}'

        if self.lead_type == 'selling' and self.buy_country is not None:
            s += f', {self.lead_type}'
        if self.lead_type == 'buying' and self.sell_country is not None:
            s += f', {self.lead_type}'

        s += f', {self.author.first_name} {self.author.last_name}, [{self.id}]'

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

    def lead_capture_url(self):
        return urljoin(settings.BASE_URL, reverse('leads:lead_capture', args=[self.id]))

    def num_contacts(self):
        return Contact.objects.filter(
            lead=self,
            deleted__isnull=True
        ).count()

    # def cover_photo(self):
    #     """Returns cover photo"""
    #     return fimods.File.objects\
    #         .filter(lead=self, deleted__isnull=True)\
    #         .order_by('-created')\
    #         .first()

    # def num_applications(self):
    #     """Number of applications on this lead"""
    #     return Application.objects.filter(
    #         lead=self,
    #         deleted__isnull=True
    #     ).count()

    # def display_images(self):
    #     """Returns display images."""
    #     NUM_DISPLAY_IMAGES = 1

    #     return fimods.File.objects\
    #         .filter(lead=self, deleted__isnull=True)\
    #         .order_by('-created')[:NUM_DISPLAY_IMAGES]

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

    Last updated: 17 Jun 2022, 7:24 PM
    """
    lead = models.ForeignKey(
        'Lead',
        related_name='lead_detail_views',
        related_query_name='lead_detail_views',
        on_delete=models.PROTECT,
        db_index=True        
    )
    viewer = models.ForeignKey(
        'relationships.User',
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

class Contact(Standard):
    """Contact.

    Last updated: 24 June 2022, 10:27 PM
    """
    lead = models.ForeignKey(
        'Lead',
        related_name='contacts',
        related_query_name='contacts',
        on_delete=models.PROTECT,
        db_index=True
    )

    first_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_index=True
    )
    last_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        related_name='contacts',
        related_query_name='contacts',
        on_delete=models.PROTECT,        
        null=True,
        blank=True,
        db_index=True
    )
    email = models.ForeignKey(
        'relationships.Email',
        related_name='contacts',
        related_query_name='contacts',
        on_delete=models.PROTECT,
        db_index=True,
        null=True,
        blank=True
    )
    phone_number = models.ForeignKey(
        'relationships.PhoneNumber',
        related_name='contacts',
        related_query_name='contacts',
        on_delete=models.PROTECT,
        db_index=True,
        null=True,
        blank=True
    )
    is_whatsapp = models.BooleanField(
        null=True,
        blank=True
    )
    is_wechat = models.BooleanField(
        null=True,
        blank=True
    )
    wechat_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    is_telegram = models.BooleanField(
        null=True,
        blank=True
    )
    telegram_username = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    is_line = models.BooleanField(
        null=True,
        blank=True
    )
    line_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    is_viber = models.BooleanField(
        null=True,
        blank=True
    )
    is_other = models.BooleanField(
        null=True,
        blank=True
    )
    comments = models.TextField(
        null=True,
        blank=True
    )
    is_buyer = models.BooleanField(
        null=True,
        blank=True
    )
    is_seller = models.BooleanField(
        null=True,
        blank=True
    )
    is_sell_comm = models.BooleanField(
        null=True,
        blank=True
    )
    is_buy_comm = models.BooleanField(
        null=True,
        blank=True
    )

    def is_country_match_country_code(self):
        if self.country is None or self.phone_number is None:
            return False

        return self.country.country_code == self.phone_number.country_code

    def last_note(self):
        return ContactNote.objects.filter(
            contact=self,
            deleted__isnull=True
        ).order_by('-created').first()

    def active_notes(self):
        return ContactNote.objects.filter(
            contact=self,
            deleted__isnull=True
        ).order_by('-created')

    def other_contacts(self):
        return Contact.objects\
            .filter(lead__author=self.lead.author)\
            .filter(
                Q(email=self.email) |\
                Q(phone_number=self.phone_number) |\
                (Q(wechat_id__isnull=True) & Q(wechat_id=self.wechat_id)))\
            .exclude(id=self.id)

class ContactNote(Standard):
    """Contact note.

    Last updated: 17 Jun 2022, 7:24 PM
    """
    relevance = models.CharField(
        max_length=20,
        choices=[
            ('relevant', 'Relevant'),
            ('maybe_later', 'Maybe Later'),
            ('not_relevant', 'Not Relevant')
        ],
        null=True,
        blank=True
    )
    contact = models.ForeignKey(
        'Contact',
        related_name='notes',
        related_query_name='notes',
        on_delete=models.PROTECT,
        db_index=True
    )
    body = models.TextField(
        null=True,
        blank=True
    )

class ContactAction(Standard):
    """Contact action.

    Last updated: 17 Jun 2022, 7:24 PM
    """
    contact = models.ForeignKey(
        'Contact',
        related_name='actions',
        related_query_name='actions',
        on_delete=models.PROTECT,
        db_index=True        
    )
    type = models.CharField(
        max_length=20,
        choices=[
            ('whatsapp', 'WhatsApp'),
            ('wechat', 'WeChat'),
            ('telegram', 'Telegram'),
            ('viber', 'Viber'),
            ('line', 'LINE'),
            ('copy_email', 'Copy Email'),
            ('copy_phone', 'Copy Phone')
        ],
        db_index=True
    )

class Application(Standard):
    """Agent application.

    Last updated: 28 May 2022, 9:47 PM
    """
    last_messaged = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    stopped_follow_up = models.DateTimeField(
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

    has_insights = models.BooleanField(
        blank=True,
        null=True
    )
    internal_notes = models.TextField(
        blank=True,
        null=True
    )

    # Not in use

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

    def num_messages(self):
        return ApplicationMessage.objects.filter(
            application=self
        ).count()

    def __str__(self):
        return f'{self.applicant.first_name} {self.applicant.last_name}, {self.lead.headline} [{self.id}]'

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

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name}: {self.body} [{self.id}]'

class LeadCategory(Choice):
    """Lead category.

    Last updated: 24 May 2022, 2:45 PM
    """
    class Meta:
        verbose_name_plural = 'Lead categories'




















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
    search_phrase = models.CharField(
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
    country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    category = models.CharField(
        max_length=200,
        null=True,
        blank=True,
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

    count = models.IntegerField(
        default=0,
        db_index=True
    )

    # Not in use
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

    class Meta:
        verbose_name_plural = 'Lead queries'

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