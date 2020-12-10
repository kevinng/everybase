from django.db import models
from common.models import Choice, Standard, short_text

# --- Start: Abstract models ---

expirable_invalidable_fieldnames = ['expired', 'invalidated',
    'invalidated_reason_md']
class ExpirableInvalidable(models.Model):
    received = models.DateTimeField(db_index=True)
    expired = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    invalidated = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    invalidated_reason_md = models.TextField(
        verbose_name='Invalidated reason in Markdown',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

lead_fieldnames = ['category', 'display_name', 'base_uom', 'details_md',
    'contact', 'company', 'contact_type', 'contact_type_details_md']
class Lead(models.Model):
    category = models.ForeignKey(
        'LeadCategory',
        on_delete=models.PROTECT,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        null=False,
        blank=False,
        db_index=True
    )
    display_name = models.CharField(
        max_length=100,
        null=False,
        blank=False, 
        db_index=True
    )

    base_uom = models.ForeignKey(
        'UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        verbose_name='Base UOM',
        null=False,
        blank=False,
        db_index=True
    )

    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=True,
        blank=True
    )

    links = models.ManyToManyField(
        'relationships.Link',
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        # null=True, # No effect
        blank=True,
        db_index=True
    )

    contact = models.ForeignKey(
        'relationships.Person',
        on_delete=models.PROTECT,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        null=False,
        blank=False,
        db_index=True
    )
    company = models.ForeignKey(
        'relationships.Company',
        on_delete=models.PROTECT,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        null=True,
        blank=True,
        db_index=True
    )
    contact_type = models.ForeignKey(
        'ContactType',
        on_delete=models.PROTECT,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        null=False,
        blank=False,
        db_index=True
    )
    contact_type_details_md = models.TextField(
        verbose_name='Contact type details in Markdown',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

    class Meta:
        abstract = True

commission_fieldnames = ['details_md', 'mark_up_type', 'mark_up_price_per_unit',
    'mark_up_percentage']
class Commission(models.Model):
    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=True,
        blank=True
    )
    mark_up_type = models.CharField(
        'Mark-up type',
        max_length=3,
        choices=[
            ('ppu', 'Price Per Unit'),
            ('pct', 'Percentage')
        ],
        default='ppu'
    )
    mark_up_price_per_unit = models.FloatField(
        verbose_name='Mark-up price per unit',
        null=True,
        blank=True,
        db_index=True
    )
    mark_up_percentage = models.FloatField(
        verbose_name='Mark-up percentage',
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

quote_fieldnames = ['details_md', 'incoterm', 'incoterm_country',
    'incoterm_location', 'currency', 'price', 'price_details_md',
    'deposit_percent', 'deposit_paymodes', 'remainder_paymodes',
    'payterms_details_md', 'delivery_details_md']
class Quote(models.Model):
    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=False,
        blank=False
    )

    incoterm = models.ForeignKey(
        'Incoterm',
        on_delete=models.PROTECT,
        related_name='%(class)s_items',
        related_query_name='%(class)s_items',
        null=True,
        blank=True,
        db_index=True
    )
    incoterm_country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='%(class)s_items',
        related_query_name='%(class)s_items',
        null=True,
        blank=True,
        db_index=True
    )
    incoterm_location = models.CharField(
        max_length=100,
        null=True,
        blank=True, 
        db_index=True
    )

    currency = models.ForeignKey(
        'Currency',
        on_delete=models.PROTECT,
        related_name='%(class)s_items',
        related_query_name='%(class)s_items',
        null=True,
        blank=True,
        db_index=True
    )
    price = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    price_details_md = models.TextField(
        verbose_name='Price details in Markdown',
        null=True,
        blank=True
    )

    deposit_percent = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    
    deposit_paymodes = models.ManyToManyField(
        'PaymentMode',
        related_name='%(class)s_deposit_paymodes',
        related_query_name='%(class)s_deposit_paymodes',
        blank=True,
        db_index=True
    )
    remainder_paymodes = models.ManyToManyField(
        'PaymentMode',
        related_name='%(class)s_remainder_paymodes',
        related_query_name='%(class)s_remainder_paymodes',
        blank=True,
        db_index=True
    )

    payterms_details_md = models.TextField(
        verbose_name='Payment terms details in Markdown',
        null=True,
        blank=True
    )
    delivery_details_md = models.TextField(
        verbose_name='Delivery details in Markdown',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

# --- End: Abstract models ---

# --- Start: Choice Models ---

class Incoterm(Choice):
    pass

class Currency(Choice):
    class Meta:
        verbose_name_plural = 'Currencies'

class PaymentMode(Choice):
    pass

class ContactType(Choice):
    pass

class LeadCategory(Choice):
    parents = models.ManyToManyField(
        'self',
        related_name='children',
        related_query_name='children',
        # null=True, # No effect
        blank=True,
        db_index=True
    )
    class Meta:
        verbose_name_plural = 'Lead categories'

class MatchMethod(Choice):
    pass

class MatchStatus(Choice):
    class Meta:
        verbose_name_plural = 'Match statuses'

class SupplyQuoteStatus(Choice):
    class Meta:
        verbose_name_plural = 'Supply quote statuses'

class DemandQuoteStatus(Choice):
    class Meta:
        verbose_name_plural = 'Demand quote statuses'

class UnitOfMeasure(Choice):
    category = models.ForeignKey(
        'LeadCategory',
        on_delete=models.PROTECT,
        related_name='unit_of_measures',
        related_query_name='unit_of_measures',
        null=False,
        blank=False,
        db_index=True
    )
    parents = models.ManyToManyField(
        'UnitOfMeasure',
        through='UOMRelationship',
        through_fields=('child', 'parent'),
        related_name='children',
        related_query_name='children',
        db_index=True
    )

class UOMRelationship(models.Model):
    child = models.ForeignKey(
        'UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='parent_uom_relationship',
        related_query_name='parent_uom_relationship',
        null=False,
        blank=False,
        db_index=True
    )
    parent = models.ForeignKey(
        'UnitOfMeasure',
        on_delete=models.PROTECT,
        related_name='child_uom_relationship',
        related_query_name='child_uom_relationship',
        null=False,
        blank=False,
        db_index=True
    )
    multiple = models.FloatField(
        null=False,
        blank=False,
        db_index=True
    )
    details_md = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'UOM relationship'
        verbose_name_plural = 'UOM relationships'
    
    def __str__(self):
        return f'(Child: {self.child}, parent: {self.parent} [{self.id}])'

# --- End: Choice Models ---

# --- Start: Main models ---

class Supply(Standard, Lead, ExpirableInvalidable):
    class Meta:
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'

class Demand(Standard, Lead, ExpirableInvalidable):
    pass

class SupplyQuote(Standard, Quote, ExpirableInvalidable):
    supply = models.ForeignKey(
        'Supply',
        on_delete=models.PROTECT,
        related_name='quotes',
        related_query_name='quotes',
        null=False,
        blank=False,
        db_index=True
    )

    status = models.ForeignKey(
        'SupplyQuoteStatus',
        on_delete=models.PROTECT,
        related_name='quotes',
        related_query_name='quotes',
        null=False,
        blank=False,
        db_index=True
    )
    packing_details_md = models.TextField(
        verbose_name='Packing details in Markdown',
        null=True,
        blank=True
    )

    downstreams = models.ManyToManyField(
        'self',
        related_name='upstreams',
        related_query_name='upstreams',
        blank=True,
        db_index=True
    )

    demand_quotes = models.ManyToManyField(
        'DemandQuote',
        through='Match',
        through_fields=('supply_quote', 'demand_quote'),
        related_name='supply_quotes',
        related_query_name='supply_quotes',
        db_index=True
    )

class ProductionCapability(Standard):
    supply_quote = models.ForeignKey(
        'SupplyQuote',
        on_delete=models.PROTECT,
        related_name='production_capabilities',
        related_query_name='production_capabilities',
        null=False,
        blank=False,
        db_index=True
    )

    start = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    end = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )

    capacity_quantity = models.FloatField(
        null=False,
        blank=False,
        db_index=True
    )
    capacity_seconds = models.FloatField(
        null=False,
        blank=False,
        db_index=True
    )

    details_md = models.TextField(
        verbose_name='Details in markdown',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Production capability'
        verbose_name_plural = 'Production capabilities'

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

class DemandQuote(Standard, Quote, ExpirableInvalidable):
    demand = models.ForeignKey(
        'Demand',
        on_delete=models.PROTECT,
        related_name='quotes',
        related_query_name='quotes',
        null=False,
        blank=False,
        db_index=True
    )

    status = models.ForeignKey(
        'DemandQuoteStatus',
        on_delete=models.PROTECT,
        related_name='quotes',
        related_query_name='quotes',
        null=False,
        blank=False,
        db_index=True
    )
    details_as_received_md = models.TextField(
        verbose_name='Details as received in Markdown',
        null=True,
        blank=True
    )
    positive_origin_countries = models.ManyToManyField(
        'common.Country',
        related_name='positive_origin_of_demand_quotes',
        related_query_name='positive_origin_of_demand_quotes',
        blank=True,
        db_index=True
    )
    negative_origin_countries = models.ManyToManyField(
        'common.Country',
        related_name='negative_origin_of_demand_quotes',
        related_query_name='negative_origin_of_demand_quotes',
        blank=True,
        db_index=True
    )
    negative_details_md = models.TextField(
        verbose_name='Negative details in Markdown',
        null=True,
        blank=True
    )

class Trench(models.Model):
    quantity = models.FloatField(
        null=False,
        blank=False,
        db_index=True
    )
    after_deposit_seconds = models.FloatField(
        verbose_name='Seconds after deposit',
        null=True,
        blank=True,
        db_index=True
    )
    paymode = models.ForeignKey(
        'PaymentMode',
        on_delete=models.PROTECT,
        related_name='trenches',
        related_query_name='trenches',
        verbose_name='Payment Mode',
        null=True,
        blank=True,
        db_index=True
    )
    payment_before_release = models.BooleanField(default=True)
    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=True,
        blank=True
    )

    # At least one of the following must be set.
    supply_quote = models.ForeignKey(
        'SupplyQuote',
        on_delete=models.PROTECT,
        related_name='trenches',
        related_query_name='trenches',
        verbose_name='Supply Quote',
        null=True,
        blank=True,
        db_index=True
    )
    demand_quote = models.ForeignKey(
        'DemandQuote',
        on_delete=models.PROTECT,
        related_name='trenches',
        related_query_name='trenches',
        verbose_name='Demand Quote',
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Trench'
        verbose_name_plural = 'Trenches'

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

class Match(Standard):
    demand_quote = models.ForeignKey(
        'DemandQuote',
        on_delete=models.PROTECT,
        related_name='matches',
        related_query_name='matches',
        null=False,
        blank=False,
        db_index=True
    )
    supply_quote = models.ForeignKey(
        'SupplyQuote',
        on_delete=models.PROTECT,
        related_name='matches',
        related_query_name='matches',
        null=False,
        blank=False,
        db_index=True
    )

    status = models.ForeignKey(
        'MatchStatus',
        on_delete=models.PROTECT,
        related_name='matches',
        related_query_name='matches',
        null=True,
        blank=True,
        db_index=True
    )
    method = models.ForeignKey(
        'MatchMethod',
        on_delete=models.PROTECT,
        related_name='matches',
        related_query_name='matches',
        null=True,
        blank=True,
        db_index=True
    )
    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

class SupplyCommission(Standard, Commission, ExpirableInvalidable):
    quotes = models.ManyToManyField(
        'SupplyQuote',
        related_name='commissions',
        related_query_name='commissions',
        blank=True,
        db_index=True
    )
    supply = models.ForeignKey(
        'Supply',
        on_delete=models.PROTECT,
        related_name='commissions',
        related_query_name='commissions',
        null=True,
        blank=True,
        db_index=True
    )

    # One of following must be set
    person = models.ForeignKey(
        'relationships.Person',
        on_delete=models.PROTECT,
        related_name='supply_commissions',
        related_query_name='supply_commissions',
        null=True,
        blank=True,
        db_index=True
    )
    company = models.ForeignKey(
        'relationships.Company',
        on_delete=models.PROTECT,
        related_name='supply_commissions',
        related_query_name='supply_commissions',
        null=True,
        blank=True,
        db_index=True
    )

class DemandCommission(Standard, Commission, ExpirableInvalidable):
    quotes = models.ManyToManyField(
        'DemandQuote',
        related_name='commissions',
        related_query_name='commissions',
        blank=True,
        db_index=True
    )
    demand = models.ForeignKey(
        'Demand',
        on_delete=models.PROTECT,
        related_name='commissions',
        related_query_name='commissions',
        null=True,
        blank=True,
        db_index=True
    )

    # One of following must be set
    person = models.ForeignKey(
        'relationships.Person',
        on_delete=models.PROTECT,
        related_name='demand_commissions',
        related_query_name='demand_commissions',
        null=True,
        blank=True,
        db_index=True
    )
    company = models.ForeignKey(
        'relationships.Company',
        on_delete=models.PROTECT,
        related_name='demand_commissions',
        related_query_name='demand_commissions',
        null=True,
        blank=True,
        db_index=True
    )

# --- End: Main models ---