from django.db import models
from common.models import (fk, m2m, m2mt, tf, cf, dtf, uid, eml, pintf, 
    Standard, Choice, short_text)

class GmassCampaignResult(Standard):
    email_address = cf(null=True)
    first_name = cf(null=True)
    last_name = cf(null=True)
    name_1 = cf(null=True)
    opens = pintf(null=True)
    clicks = pintf(null=True)
    replied = cf(null=True)
    unsubscribed = cf(null=True)
    bounced = cf(null=True)
    blocked = cf(null=True)
    over_gmail_limit = cf(null=True)
    bounce_reason = tf(null=True)
    gmail_response = cf(null=True)

    email = fk('relationships.Email', 'gmass_campaign_results', null=True)
    gmass_campaign = fk('GmassCampaign', 'results', null=True)

    def __str__(self):
        return f'({self.email_address} [{self.id}])'

class GmassCampaign(Standard):
    sent = dtf(null=True)
    campaign_id = cf()
    subject = cf(null=True)
    spreadsheet = cf(null=True)

    def __str__(self):
        return f'({self.campaign_id}, {self.sent} [{self.id}])'

class ChemicalClusterOfSingaporeResult(Standard):
    harvested = dtf(null=True)
    source_link = cf(null=True)
    
    company_name = cf(null=True)
    telephone = cf(null=True)
    fax = cf(null=True)
    email_str = cf(null=True)
    website = cf(null=True)
    address_str = cf(null=True, db_index=False)

    company = fk('relationships.Company',
        'chemical_cluster_of_singapore_results', null=True)
    
    email = fk('relationships.Email',
        'chemical_cluster_of_singapore_results', null=True)

    phone_number = fk('relationships.PhoneNumber',
        'chemical_cluster_of_singapore_results', null=True)

    link = fk('relationships.Link',
        'chemical_cluster_of_singapore_results', null=True)

    address = fk('relationships.Address',
        'chemical_cluster_of_singapore_results', null=True)

    class Meta:
        verbose_name = 'ChemicalClusterOfSingapore result'
        verbose_name_plural = 'ChemicalClusterOfSingapore results'

    def __str__(self):
        return f'({self.company_name}, {self.harvested} [{self.id}])'

class Fibre2FashionBuyingOffer(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='fibre2fashion_buying_offers',
        related_query_name='fibre2fashion_buying_offers',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    harvested = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

    source_link = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        db_index=True
    )
    category = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    sub_category = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    title = models.TextField(
        null=True,
        blank=True
    )
    reference_no = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    email_str = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    product_info_html = models.TextField(
        null=True,
        blank=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='fibre2fashion_buying_offer_emails',
        related_query_name='fibre2fashion_buying_offer_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='fibre2fashion_buying_offer_invalid_emails',
        related_query_name='fibre2fashion_buying_offer_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Fibre2Fashion buying offer'
        verbose_name_plural = 'Fibre2Fashion buying offers'

    def __str__(self):
        return f'({short_text(self.title)}, {self.email_str} [{self.id}])'

class Fibre2FashionSellingOffer(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='fibre2fashion_selling_offers',
        related_query_name='fibre2fashion_selling_offers',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    harvested = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

    source_link = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        db_index=True
    )
    category = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    sub_category = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    title = models.TextField(
        null=True,
        blank=True
    )
    reference_no = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    email_str = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    company_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    company_address = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
    product_info_html = models.TextField(
        null=True,
        blank=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='fibre2fashion_selling_offer_emails',
        related_query_name='fibre2fashion_selling_offer_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='fibre2fashion_selling_offer_invalid_emails',
        related_query_name='fibre2fashion_selling_offer_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Fibre2Fashion selling offer'
        verbose_name_plural = 'Fibre2Fashion selling offers'

    def __str__(self):
        return f'({short_text(self.title)}, {self.email_str} [{self.id}])'

class ZeroBounceResult(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='zero_bounce_results',
        related_query_name='zero_bounce_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    generated = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

    email_str = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True
    )
    status = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        db_index=True,
        choices=[
            ('valid', 'Valid'),
            ('invalid', 'Invalid'),
            ('catch-all', 'Catch-All'),
            ('spamtrap', 'Spamtrap'),
            ('abuse', 'Abuse'),
            ('do_not_mail', 'Do Not Mail'),
            ('unknown', 'Unknown')
        ]
    )
    sub_status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        choices=[
            ('antispam_system', 'Anti-Spam System'),
            ('does_not_accept_mail', 'Does Not Accept Mail'),
            ('exception_occurred', 'Exception Occurred'),
            ('failed_smtp_connection', 'Failed SMTP Connection'),
            ('failed_syntax_check', 'Failed Syntax Check'),
            ('forcible_disconnect', 'Forcible Disconnect'),
            ('global_suppression', 'Global Suppression'),
            ('greylisted', 'Greylisted'),
            ('leading_period_removed', 'Leading Period Removed'),
            ('mail_server_did_not_respond', 'Mail Server Did Not Respond'),
            ('mail_server_temporary_error', 'Mail Server Temporary Error'),
            ('mailbox_quota_exceeded', 'Mailbox Quota Exceeded'),
            ('mailbox_not_found', 'Mailbox Not Found'),
            ('no_dns_entries', 'No DNS Entries'),
            ('possible_trap', 'Possible Trap'),
            ('possible_typo', 'Possible Typo'),
            ('role_based', 'Role-Based'),
            ('timeout_exceeded', 'Timeout Exceeded'),
            ('unroutable_ip_address', 'Unroutable IP Address'),
            ('alias_address', 'Alias Address'),
            ('role_based_catch_all', 'Role-Based Catch-All'),
            ('disposable', 'Disposable'),
            ('toxic', 'Toxic')
        ]
    )
    account = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    domain = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    gender = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    free_email = models.BooleanField(
        null=False,
        blank=False,
        db_index=True
    )
    mx_found = models.BooleanField(
        null=False,
        blank=False,
        db_index=True
    )
    mx_record = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    smtp_provider = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    did_you_mean = models.EmailField(
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='zero_bounce_result_emails',
        related_query_name='zero_bounce_result_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='zero_bounce_result_invalid_emails',
        related_query_name='zero_bounce_result_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    did_you_mean_email = models.ForeignKey(
        'relationships.Email',
        related_name='zero_bounce_result_did_you_mean_emails',
        related_query_name='zero_bounce_result_did_you_mean_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'ZeroBounce result'
        verbose_name_plural = 'ZeroBounce results'
    
    def __str__(self):
        return f'({self.email_str} [{self.id}])'

class DataSource(Choice):
    emails = m2mt(
        'relationships.Email',
        'SourcedEmail',
        'source', 'email',
        'data_sources')

class SourcedEmail(Standard):
    harvested = dtf(null=True)

    source = fk('DataSource', 'sourced_emails')
    email = fk('relationships.Email', 'sourced_emails')

    def __str__(self):
        return f'({self.email_address} [{self.id}])'

class ChemicalBookSupplier(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='chemical_book_results',
        related_query_name='chemical_book_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    harvested = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

    source_url = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        db_index=True
    )
    company_name = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_index=True
    )
    internal_url = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_index=True
    )
    telephone = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    email_str = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    corporate_site_url = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_index=True
    )
    nationality = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='chemical_book_result_emails',
        related_query_name='chemical_book_result_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='chemical_book_result_invalid_emails',
        related_query_name='chemical_book_result_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Chemical Book Result'
        verbose_name_plural = 'Chemical Book Results'

    def __str__(self):
        return f'({self.company_name} [{self.id}])'

class LookChemSupplier(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='look_chem_results',
        related_query_name='look_chem_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    harvested = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

    coy_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    contact_person = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    street_address = models.TextField(
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    province_state = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    country_region = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    zip_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    business_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    tel = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    mobile = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    email_str = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    website = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    qq = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='look_chem_result_emails',
        related_query_name='look_chem_result_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='look_chem_result_invalid_emails',
        related_query_name='look_chem_result_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'LookChem supplier'
        verbose_name_plural = 'LookChem suppliers'

    def __str__(self):
        return f'({self.coy_name} [{self.id}])'

class WorldOfChemicalsSupplier(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='world_of_chemicals_supplier_results',
        related_query_name='world_of_chemicals_supplier_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    harvested = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

    source_url = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_index=True
    )
    coy_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_about_html = models.TextField(
        null=True,
        blank=True
    )
    coy_pri_contact = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_addr_1 = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    coy_addr_2 = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )
    coy_city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_state = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_postal = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_phone = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_phone_2 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_owner_email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_alt_email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_alt_email_2 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_alt_email_3 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    coy_website = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='world_of_chemicals_supplier_emails',
        related_query_name='world_of_chemicals_supplier_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    owner_email = models.ForeignKey(
        'relationships.Email',
        related_name='world_of_chemicals_supplier_owner_emails',
        related_query_name='world_of_chemicals_supplier_owner_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    alt_email = models.ForeignKey(
        'relationships.Email',
        related_name='world_of_chemicals_supplier_alt_emails',
        related_query_name='world_of_chemicals_supplier_alt_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    alt_email_2 = models.ForeignKey(
        'relationships.Email',
        related_name='world_of_chemicals_supplier_alt_email_2s',
        related_query_name='world_of_chemicals_supplier_alt_email_2s',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    alt_email_3 = models.ForeignKey(
        'relationships.Email',
        related_name='world_of_chemicals_supplier_alt_email_3s',
        related_query_name='world_of_chemicals_supplier_alt_email_3s',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='world_of_chemicals_supplier_invalid_emails',
        related_query_name='world_of_chemicals_supplier_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_owner_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='world_of_chemicals_supplier_invalid_owner_emails',
        related_query_name='world_of_chemicals_supplier_invalid_owner_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_alt_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='world_of_chemicals_supplier_invalid_alt_emails',
        related_query_name='world_of_chemicals_supplier_invalid_alt_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_alt_email_2 = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='world_of_chemicals_supplier_invalid_alt_email_2s',
        related_query_name='world_of_chemicals_supplier_invalid_alt_email_2s',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_alt_email_3 = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='world_of_chemicals_supplier_invalid_alt_email_3s',
        related_query_name='world_of_chemicals_supplier_invalid_alt_email_3s',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    
    def __str__(self):
        return f'({self.coy_name} [{self.id}])'

class OKChemResult(Standard):
    harvested = dtf(null=True)

    name = cf(null=True)
    country = cf(null=True)
    request = cf(null=True)
    email = cf(null=True)
    
    class Meta:
        verbose_name = 'OKChem result'
        verbose_name_plural = 'OKChem results'
    
    def __str__(self):
        return f'({self.email} [{self.id}])'