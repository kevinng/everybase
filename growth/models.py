from django.core.exceptions import ValidationError

from django.db import models
from common.models import Standard, short_text

class GmassEmailStatus(Standard):
    bounced = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    bounce_reason = models.TextField(
        null=True,
        blank=True
    )
    unsubscribed = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

    email = models.OneToOneField(
        'relationships.Email',
        related_name='gmass_email_status',
        related_query_name='gmass_email_status',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.OneToOneField(
        'relationships.InvalidEmail',
        related_name='gmass_email_status',
        related_query_name='gmass_email_status',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Gmass email status'
        verbose_name_plural = 'Gmass email statuses'

    def __str__(self):
        email_str = self.email if self.email is not None else self.invalid_email
        return f'({email_str} [{self.id}])'

class GmassCampaignResult(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='gmass_campaign_results',
        related_query_name='gmass_campaign_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    email_address = models.CharField(
        max_length=400,
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
    name_1 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    opens = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    clicks = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    replied = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    unsubscribed = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    bounced = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    blocked = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    over_gmail_limit = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    gmail_response = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='gmass_campaign_results',
        related_query_name='gmass_campaign_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='gmass_campaign_results',
        related_query_name='gmass_campaign_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    gmass_campaign = models.ForeignKey(
        'GmassCampaign',
        related_name='gmass_campaign_results',
        related_query_name='gmass_campaign_results',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.email_address} [{self.id}])'

class GmassCampaign(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='gmass_campaigns',
        related_query_name='gmass_campaigns',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    sent = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    campaign_id = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        db_index=True
    )
    subject = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    spreadsheet = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    report_url = models.URLField(
        null=False,
        blank=False,
        db_index=True
    )
    report_last_accessed = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'({self.campaign_id}, {self.sent} [{self.id}])'

class ChemicalClusterOfSingaporeCompany(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='chemical_cluster_of_singapore_companies',
        related_query_name='chemical_cluster_of_singapore_companies',
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
    company_name = models.CharField(
        max_length=100,
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
    fax = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    email_str = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    website = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        db_index=True
    )
    address = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        db_index=True
    )
    nature_of_business = models.TextField(
        null=True,
        blank=True
    )
    executive_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    executive_telephone = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    executive_email_str = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='chemical_cluster_of_singapore_company_emails',
        related_query_name='chemical_cluster_of_singapore_company_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='chemical_cluster_of_singapore_company_invalid_emails',
        related_query_name=
            'chemical_cluster_of_singapore_company_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    executive_email = models.ForeignKey(
        'relationships.Email',
        related_name='chemical_cluster_of_singapore_company_executive_emails',
        related_query_name=
            'chemical_cluster_of_singapore_company_executive_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_executive_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name=
            'chemical_cluster_of_singapore_company_invalid_executive_emails',
        related_query_name=
            'chemical_cluster_of_singapore_company_invalid_executive_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Chemical Cluster of Singapore company'
        verbose_name_plural = 'Chemical Cluster of Singapore companies'

    def __str__(self):
        return f'({self.company_name}, {self.harvested} [{self.id}])'

class ChemicalClusterOfSingaporeProduct(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='chemical_cluster_of_singapore_products',
        related_query_name='chemical_cluster_of_singapore_products',
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
    company_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    product = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

class ChemicalClusterOfSingaporeService(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='chemical_cluster_of_singapore_services',
        related_query_name='chemical_cluster_of_singapore_services',
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
    company_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    service = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

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

    source_url = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        unique=True,
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
        max_length=400,
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

    source_url = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        unique=True,
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
        max_length=400,
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
        max_length=400,
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

class ChemicalBookSupplier(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='chemical_book_suppliers',
        related_query_name='chemical_book_suppliers',
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
        max_length=400,
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
        related_name='chemical_book_supplier_emails',
        related_query_name='chemical_book_supplier_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='chemical_book_supplier_invalid_emails',
        related_query_name='chemical_book_supplier_invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Chemical Book supplier'
        verbose_name_plural = 'Chemical Book suppliers'

    def __str__(self):
        return f'({self.company_name} [{self.id}])'

class LookChemSupplier(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='look_chem_suppliers',
        related_query_name='look_chem_suppliers',
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

    company_name = models.CharField(
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
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    website = models.CharField(
        max_length=300,
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
        return f'({self.company_name} [{self.id}])'

class WorldOfChemicalsSupplier(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='world_of_chemicals_suppliers',
        related_query_name='world_of_chemicals_suppliers',
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
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    coy_owner_email = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    coy_alt_email = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    coy_alt_email_2 = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    coy_alt_email_3 = models.CharField(
        max_length=400,
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

class OKChemBuyingRequest(Standard):
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='ok_chem_buying_requests',
        related_query_name='ok_chem_buying_requests',
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

    name = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    request = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
    email = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    domain = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        db_index=True
    )
    
    class Meta:
        verbose_name = 'OKChem buying request'
        verbose_name_plural = 'OKChem buying requests'
    
    def __str__(self):
        return f'({self.email} [{self.id}])'

class Note(Standard):
    """Note/task related to a contact (e.g., email, phone number). The contact
    may not have an associated user in our database because the user hasn't
    contacted the chatbot.

    Last updated: 11 August 2021, 2:46 PM
    """

    phone_number = models.ForeignKey(
        'relationships.PhoneNumber',
        related_name='growth_notes',
        related_query_name='growth_notes',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    email = models.ForeignKey(
        'relationships.Email',
        related_name='growth_notes',
        related_query_name='growth_notes',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    note_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=[
            ('onboarding', 'Onboarding'),
            ('information', 'Information'),
            ('task', 'Task')
        ]
    )

    text = models.TextField(
        null=True,
        blank=True,
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True
    )
    done = models.DateTimeField(
        null=True,
        blank=True
    )

    def clean(self):
        super(Note, self).clean()

        # Either phone_number or email must be set
        if self.phone_number is None and self.email is None:
            raise ValidationError('Either phone_number or email must be set')