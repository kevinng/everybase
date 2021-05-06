from django.db import models

from django.core.exceptions import ValidationError

from common.models import Standard, short_text

class TestMessage(Standard):
    """Message for testing purposes.

    Last updated: 4 May 2021, 3:40 PM
    """
    body = models.TextField()

    def __str__(self):
        return f'({short_text(self.body)} [{self.id}])'

class MessageBodyMetaData(Standard):
    """Meta data generated for a message body - test or production.

    Last updated: 4 May 2021, 1:14 PM
    """
    group = models.CharField(
        max_length=200,
        db_index=True
    )
    ran = models.DateField(db_index=True)
    is_base_truth = models.BooleanField(db_index=True)
    is_enabled = models.BooleanField(db_index=True)
    version = models.CharField(
        max_length=200,
        db_index=True
    )
    body_copy = models.TextField()
	
    # Either 1 must be set
    twilio_inbound_message = models.ForeignKey(
        'chat.TwilioInboundMessage',
        related_name='message_body_meta_datas',
        related_query_name='message_body_meta_datas',
        on_delete=models.PROTECT,
        db_index=True
    )
    test_message = models.ForeignKey(
        'TestMessage',
        related_name='message_body_meta_datas',
        related_query_name='message_body_meta_datas',
        on_delete=models.PROTECT,
        db_index=True
    )

    def clean(self):
        super(MessageBodyMetaData, self).clean()

        if self.twilio_inbound_message is None and self.test_message is None:
            raise ValidationError('Either twilio_inbound_message or \
                test_message must be set.')

    def __str__(self):
        return f'({self.group}, {self.ran}, {short_text(self.body_copy)} \
            [{self.id}])'

class MessageBodyMetaDataEntity(Standard):
    """Entity of a message's body meta data.

    Last updated: 4 May 2021, 5:30 PM
    """
    entity_type = models.CharField(
        max_length=30,
        choices=[
            ('newline', 'Newline'),
            ('domain_dot', 'Domain Dot'),
            ('tld', 'TLD'),
            ('url', 'URL'),
            ('decimal_point', 'Decimal Point'),
            ('number_separator', 'Number Separator'),
            ('number_uom', 'Number UOM'),
            ('number', 'Number'),
            ('fullstop', 'Fullstop'),
            ('exclamation_mark', 'Exclamation Mark'),
            ('email', 'Email'),
            ('currency', 'Currency'),
            ('price', 'Price'),
            ('excluded_price', 'Excluded Price'),
            ('location', 'Location'),
            ('incoterm_availability', 'Incoterm/Availability'),
            ('application', 'Application'),
            ('phone_number', 'Phone Number'),
            ('company', 'Company'),
            ('product_type', 'Product Type'),
            ('product', 'Product'),
            ('product_specification_type', 'Product Specification Type'),
            ('uom', 'UOM'),
            ('moq', 'MOQ'),
            ('quantity', 'Quantity'),
            ('packing', 'Packing')
        ],
        db_index=True
    )
    start_position = models.IntegerField(db_index=True)
    end_position = models.IntegerField(db_index=True)
    boolean_value = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    numeric_value = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    string_value = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    substring = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    programmatic_key_1 = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    programmatic_key_2 = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    meta_data = models.ForeignKey(
        'MessageBodyMetaData',
        related_name='message_body_meta_datas',
        related_query_name='message_body_meta_datas',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.entity_type}, {self.substring}, \
            {short_text(self.meta_data)} [{self.id}])'

    class Meta:
        verbose_name = 'Message body meta data entity'
        verbose_name_plural = 'Message body meta data entities'

class MatchingKeyword(Standard):
    """A keyword we need to match for a certain entity.

    Last updated: 5 May 2021, 3:39 PM
    """
    keyword = models.CharField(
        max_length=200,
        db_index=True
    )
    case_sensitive = models.BooleanField(
        default=False,
        db_index=True
    )
    edit_distance_tolerance = models.IntegerField(db_index=True)

    # Set either 1
    currency = models.ForeignKey(
        'payments.Currency',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    excluded_price = models.ForeignKey(
        'relationships.ExcludedPrice',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    location = models.ForeignKey(
        'relationships.Location',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    incoterm_availability = models.ForeignKey(
        'relationships.IncotermAvailability',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    application = models.ForeignKey(
        'relationships.Application',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    company = models.ForeignKey(
        'relationships.Company',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    product_type = models.ForeignKey(
        'relationships.ProductType',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    product = models.ForeignKey(
        'relationships.Product',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    product_specification_type = models.ForeignKey(
        'relationships.ProductSpecificationType',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    unit_of_measure = models.ForeignKey(
        'relationships.UnitOfMeasure',
        related_name='matching_keywords',
        related_query_name='matching_keywords',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def clean(self):
        super(MatchingKeyword, self).clean()

        count = 0

        if self.currency is not None:
            count += 1

        if self.excluded_price is not None:
            count += 1

        if self.location is not None:
            count += 1

        if self.incoterm_availability is not None:
            count += 1

        if self.application is not None:
            count += 1

        if self.company is not None:
            count += 1

        if self.product_type is not None:
            count += 1

        if self.product is not None:
            count += 1

        if self.product_specification_type is not None:
            count += 1

        if self.unit_of_measure is not None:
            count += 1

        if count != 1:
            raise ValidationError('Either currency, excluded price, location, \
                incoterm/availability, application, company, product type, \
                product, product specification type or unit of measure must be \
                set.')

        # We don't use PositiveIntegerField because there's a debate on whether
        # it should accept 0. It could change in the future.
        if self.edit_distance_tolerance < 0:
            raise ValidationError('Edit distance must be 0 or greater.')