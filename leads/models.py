from django.db import models
from common.models import fk, m2m, m2mt, tf, cf, ff, dtf
from common.models import Choice, Standard, short_text

# --- Start: Abstract models ---

expirable_invalidable_fieldnames = ['expired', 'invalidated',
    'invalidated_reason_md']
class ExpirableInvalidable(models.Model):
    expired = dtf(null=True)
    invalidated = dtf(null=True)
    invalidated_reason_md = tf('Invalidated reason in Markdown', True)

    class Meta:
        abstract = True

lead_fieldnames = ['category', 'display_name', 'base_uom', 'details_md',
    'files', 'contact', 'company', 'contact_type', 'contact_type_details_md']
class Lead(models.Model):
    category = fk('LeadCategory', '%(class)s_leads')
    display_name = cf()

    base_uom = fk('UnitOfMeasure', '%(class)s_leads', 'Base UOM')

    details_md = tf('Details in Markdown', True)
    files = m2m('files.File', '%(class)s_leads', True)

    contact = fk('relationships.Person', '%(class)s_leads')
    company = fk('relationships.Company', '%(class)s_leads', null=True)
    contact_type = fk('ContactType', '%(class)s_leads')
    contact_type_details_md = tf('Contact type details in Markdown', True)

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

    class Meta:
        abstract = True

commission_fieldnames = ['details_md', 'mark_up_type', 'mark_up_price_per_unit',
    'mark_up_percentage']
class Commission(models.Model):
    details_md = tf('Details in Markdown', True)
    mark_up_type = models.CharField(
        'Mark-up type',
        max_length=3,
        choices=[
            ('ppu', 'Price Per Unit'),
            ('pct', 'Percentage')
        ],
        default='ppu'
    )
    mark_up_price_per_unit = ff('Mark-up price per unit', True)
    mark_up_percentage = ff('Mark-up percentage', True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

quote_fieldnames = ['details_md', 'incoterm', 'incoterm_country',
    'incoterm_location', 'currency', 'price', 'price_details_md',
    'deposit_percent', 'deposit_paymodes', 'remainder_paymodes',
    'payterms_details_md', 'delivery_details_md']
class Quote(models.Model):
    details_md = tf('Details in Markdown')

    incoterm = fk('Incoterm', '%(class)s_items', null=True)
    incoterm_country = fk('common.Country', '%(class)s_items', null=True)
    incoterm_location = cf(null=True)
    currency = fk('Currency', '%(class)s_items', null=True)
    price = ff(null=True)
    price_details_md = tf('Price details in Markdown', True)

    deposit_percent = ff(null=True)
    
    deposit_paymodes = m2m('PaymentMode', '%(class)s_deposit_paymodes', True)
    remainder_paymodes = m2m('PaymentMode', '%(class)s_remainder_paymodes', True)

    payterms_details_md = tf('Payment terms details in Markdown', True)
    delivery_details_md = tf('Delivery details in Markdown', True)

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
    parent = fk('self', 'children', null=True)
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
    multiple = ff()
    details_md = tf(null=True)

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
    supply = fk('Supply', 'quotes')

    status = fk('SupplyQuoteStatus', 'quotes')
    packing_details_md = tf('Packing details in Markdown', True)

    downstreams = m2m('self', 'upstreams', True)

    demand_quotes = m2mt(
        'DemandQuote',
        'Match',
        'supply_quote', 'demand_quote',
        'supply_quotes'
    )

class ProductionCapability(Standard):
    supply_quote = fk('SupplyQuote', 'production_capabilities')

    start = dtf(null=True)
    end = dtf(null=True, default=None)

    capacity_quantity = ff()
    capacity_seconds = ff()

    details_md = tf('Details in markdown', null=True)

    class Meta:
        verbose_name = 'Production capability'
        verbose_name_plural = 'Production capabilities'

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

class DemandQuote(Standard, Quote, ExpirableInvalidable):
    demand = fk('Demand', 'quotes')

    status = fk('DemandQuoteStatus', 'quotes')
    details_as_received_md = tf('Details as received in Markdown', null=True)
    positive_origin_countries = m2m(
        'common.Country', 'positive_origin_of_demand_quotes', True)
    negative_origin_countries = m2m(
        'common.Country', 'negative_origin_of_demand_quotes', True)
    negative_details_md = tf('Negative details in Markdown', null=True)

class Trench(models.Model):
    quantity = ff()
    after_deposit_seconds = ff('Seconds after deposit', True)
    paymode = fk('PaymentMode', 'trenches', 'Payment Mode', True)
    payment_before_release = models.BooleanField(default=True)
    details_md = tf('Details in Markdown', True)

    # At least one of the following must be set.
    supply_quote = fk('SupplyQuote', 'trenches', 'Supply Quote', True)
    demand_quote = fk('DemandQuote', 'trenches', 'Demand Quote', True)

    class Meta:
        verbose_name = 'Trench'
        verbose_name_plural = 'Trenches'

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

class Match(Standard):
    demand_quote = fk('DemandQuote', 'matches')
    supply_quote = fk('SupplyQuote', 'matches')

    status = fk('MatchStatus', 'matches', null=True)
    method = fk('MatchMethod', 'matches', null=True)
    details_md = tf('Details in Markdown', True)

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    def __str__(self):
        return f'({short_text(self.details_md)} [{self.id}])'

class SupplyCommission(Standard, Commission, ExpirableInvalidable):
    quotes = m2m('SupplyQuote', 'commissions', True)
    supply = fk('Supply', 'commissions', null=True)

    # One of following must be set
    person = fk('relationships.Person', 'supply_commissions', null=True)
    company = fk('relationships.Company', 'supply_commissions', null=True)

class DemandCommission(Standard, Commission, ExpirableInvalidable):
    quotes = m2m('DemandQuote', 'commissions', True)
    demand = fk('Demand', 'commissions', null=True)

    # One of following must be set
    person = fk('relationships.Person', 'demand_commissions', null=True)
    company = fk('relationships.Company', 'demand_commissions', null=True)

# --- End: Main models ---