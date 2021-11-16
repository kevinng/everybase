from datetime import datetime
import uuid, pytz
from django.db import models

from common.models import Standard
from files import models as fimods
from everybase import settings

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

    def created_now_difference(self):
        sgtz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.now(tz=sgtz)
        difference = (now - self.created).total_seconds()
        
        weeks, rest = divmod(difference, 604800)
        days, rest = divmod(rest, 86400)
        hours, rest = divmod(rest, 3600)
        minutes, seconds = divmod(rest, 60)

        return (weeks, days, hours, minutes, seconds)

    def create_now_difference_display_text(self):
        weeks, days, hours, minutes, seconds = self.created_now_difference()

        if weeks > 0 and weeks < 4:
            if weeks == 1:
                return '1 week ago'

            return '%d weeks ago' % weeks
        elif days > 0:
            if days == 1:
                return '1 day ago'

            return '%d days ago' % days
        elif hours > 0:
            if hours == 1:
                return '1 hour ago'

            return '%d hours ago' % hours
        elif minutes > 0:
            if minutes == 1:
                return '1 minute ago'

            return '%d minutes ago' % minutes
        elif seconds > 0:
            if seconds == 1:
                return '1 second ago'

            return '%d seconds ago' % seconds

        return self.created.strftime('%d %b %Y')

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