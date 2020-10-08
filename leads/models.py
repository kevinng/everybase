from django.db import models
from common.models import Choice, Standard, ParentChildrenChoice

# --- Start: Abstract ---

# Helper function to declare foreign key relationships.
fk = lambda klass, name, verbose_name=verbose_name: models.ForeignKey(
        klass,
        on_delete=models.PROTECT,
        related_name=name,
        related_query_name=name,
        verbose_name=verbose_name
    )

fkx = lambda klass: models.ForeignKey(klass, on_delete=models.PROTECT)

# Helper function to declare many-to-many relationships.
m2m = lambda klass, name, blank=True: models.ManyToManyField(
        klass,
        related_name=name,
        related_query_name=name,
        blank=blank
    )

# Helper function to declare many-to-many through relationships.
m2mt = lambda klass, thru, f1, f2, name: models.ManyToManyField(
        klass,
        through=thru,
        through_fields=(f1, f2),
        related_name=name,
        related_query_name=name
    )

class ExpirableInvalidable(models.Model):
    expired = models.DateTimeField(null=True, blank=True, default=None)
    invalidated = models.DateTimeField(null=True, blank=True, default=None)
    invalidated_reason_md = models.TextField('Invalidated reason in Markdown',
        null=True, blank=True, default=None)

    class Meta:
        abstract = True

class Lead(models.Model):
    category = fk('LeadCategory', '%(class)s_leads')
    display_name = models.CharField(max_length=100)

    base_uom = fk('UnitOfMeasure', '%(class)s_leads')

    details_md = models.TextField('Details in Markdown',
        null=True, blank=True)
    files = m2m('files.File', '%(class)s_leads')

    contact = fk('relationships.Person', '%(class)s_leads')
    company = fk('relationships.Company', '%(class)s_leads')
    contact_type = fk('ContactType', '%(class)s_leads')
    contact_type_details_md = models.TextField(
        'Contact type details in Markdown')

    class Meta:
        abstract = True

class Commission(models.Model):
    details_md = models.TextField()
    mark_up_type = models.CharField(
        max_length=3,
        choices=[
            ('ppu', 'Price Per Unit'),
            ('pct', 'Percentage')
        ],
        default='ppu'
    )
    mark_up_price_per_unit = models.FloatField()
    mark_up_percentage = models.FloatField()

    # At least person or company must be specified.
    person = fk('relationships.Person', '%(class)s_items')
    company = fk('relationships.Company', '%(class)s_items')

    class Meta:
        abstract = True

class Quote(models.Model):
    details_md = models.TextField()
    status = fk('QuoteStatus', '%(class)s_items')

    incoterm = fk('Incoterm', '%(class)s_items')
    incoterm_country = fk('common.Country', '%(class)s_items')
    incoterm_location = models.CharField(max_length=100)
    currency = fk('Currency', '%(class)s_items')
    price = models.FloatField()
    price_details_md = models.TextField()

    deposit_percent = models.FloatField()
    
    deposit_paymodes = m2m('PaymentMode', '%(class)s_deposit_paymodes')
    remainder_paymodes = m2m('PaymentMode', '%(class)s_remainder_paymodes')

    payterms_details_md = models.TextField()
    delivery_details_md = models.TextField()

    class Meta:
        abstract = True

# --- End: Abstract ---

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

class LeadCategory(ParentChildrenChoice):
    class Meta:
        verbose_name_plural = 'Lead categories'

class MatchMethod(Choice):
    pass

class MatchStatus(Choice):
    class Meta:
        verbose_name_plural = 'Match statuses'

class QuoteStatus(Choice):
    class Meta:
        verbose_name_plural = 'Quote statuses'

class UnitOfMeasure(Choice):
    category = fk('LeadCategory', 'unit_of_measures')
    parents = m2mt(
        'UnitOfMeasure',
        'UOMRelationship',
        'child', 'parent',
        'children'
    )

class UOMRelationship(models.Model):
    child = fk('UnitOfMeasure', 'parent_uom_relationship')
    parent = fk('UnitOfMeasure', 'child_uom_relationship')
    multiple = models.FloatField()
    details_md = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'UOM relationship'
        verbose_name_plural = 'UOM relationships'
    
    def __str__(self):
        return '[Child: %s / Parent: %s] (%d)' % (self.child, self.parent, self.id)

# --- End: Choice Models ---

# --- Start: Main models ---

class Supply(Standard, Lead, ExpirableInvalidable):
    class Meta:
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'

class Demand(Standard, Lead, ExpirableInvalidable):
    pass

class SupplyQuote(Standard, Quote, ExpirableInvalidable):
    supply = fk('Supply', 'quotes')

    packing_details_md = models.TextField()

    downstreams = m2m('self', 'upstreams')

    demand_quotes = m2mt(
        'DemandQuote',
        'Match',
        'supply_quote', 'demand_quote',
        'supply_quotes'
    )

class ProductionCapability(Standard):
    supply_quote = fk('SupplyQuote', 'production_capabilities')

    start = models.DateTimeField(null=True, default=None)
    end = models.DateTimeField(null=True, default=None)

    capacity_quantity = models.FloatField()
    capacity_seconds = models.FloatField()

    details_md = models.TextField()

class DemandQuote(Standard, Quote, ExpirableInvalidable):
    demand = fk('Demand', 'quotes')

    details_as_received_md = models.TextField()
    positive_origin_countries = m2m(
        'common.Country', 'positive_origin_of_demand_quotes')
    negative_origin_countries = m2m(
        'common.Country', 'negative_origin_of_demand_quotes')
    negative_details_md = models.TextField()

class Trench(models.Model):
    quantity = models.FloatField()
    after_deposit_seconds = models.FloatField()
    paymode = fk('PaymentMode', 'trenches')
    payment_before_release = models.BooleanField()
    details_md = models.TextField()

    # At least one of the following must be set.
    supply_quote = fk('SupplyQuote', 'trenches')
    demand_quote = fk('DemandQuote', 'trenches')

class Match(Standard):
    demand_quote = fk('DemandQuote', 'matches')
    supply_quote = fk('SupplyQuote', 'matches')

    status = fk('MatchStatus', 'matches')
    method = fk('MatchMethod', 'matches')
    details_md = models.TextField()

class SupplyCommission(Standard, Commission, ExpirableInvalidable):
    quotes = m2m('SupplyQuote', 'commissions')
    supply = fk('Supply', 'commissions')
    person = fk('relationships.Person', 'supply_commissions')
    company = fk('relationships.Company', 'supply_commissions')

class DemandCommission(Standard, Commission, ExpirableInvalidable):
    quotes = m2m('DemandQuote', 'commissions')
    demand = fk('Demand', 'commissions')
    person = fk('relationships.Person', 'demand_commissions')
    company = fk('relationships.Company', 'demand_commissions')

# --- End: Main models ---