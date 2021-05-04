from django.db import models
# from common.models import Standard, Choice, short_text
from common.models import Standard, short_text
# from django.core.exceptions import ValidationError

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
            ('excluded_pricing', 'Excluded Pricing'),
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

# class BaseTruth(Standard):
#     """Base truth - i.e., what we expect when we run a function over a message.

#     Last updated: 28 April 2021, 11:00 AM
#     """
#     message_group = models.ForeignKey(
#         'TestMessageGroup',
#         related_name='base_truths',
#         related_query_name='base_truths',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     method = models.ForeignKey(
#         'Method',
#         related_name='base_truths',
#         related_query_name='base_truths',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     expected_output = models.TextField()

#     def clean(self):
#         super(BaseTruth, self).clean()

#         count = 0
#         if self.text_output is not None:
#             count += 1

#         if self.integer_output is not None:
#             count += 1

#         if self.float_output is not None:
#             count += 1

#         # Either 1 of 3 outputs must be set.
#         if count != 1:
#             raise ValidationError('Either text_output, integer_output, \
#                 or float_output must be set.')

#     def __str__(self):
#         return f'({self.message}, {self.function} [{self.id}])'

# class InboundMessageGroup(Standard):
#     """We operate on inbound messages one group at a time. This is a group of
#     inbound messages.

#     Last updated: 28 April 2021, 3:18 AM
#     """

#     is_disabled	= models.BooleanField(db_index=True)
#     grouped = models.DateTimeField(db_index=True)
#     initial_body = models.TextField()

#     twilio_inbound_messages = models.ManyToManyField(
#         'chat.TwilioInboundMessage',
#         related_name='inbound_message_groups',
#         related_query_name='inbound_message_groups',
#         db_index=True
#     )

# class GroupingMethod(Standard, Choice):
#     """Method used to group a group of Twilio inbound messages.

#     Last updated: 23 April 2021, 1:13 PM
#     """

#     applied = models.DateTimeField(db_index=True)
#     order = models.IntegerField(db_index=True)
	
#     inbound_message_group = models.ForeignKey(
#         'InboundMessageGroup',
#         related_name='grouping_methods',
#         related_query_name='grouping_methods',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     method = models.ForeignKey(
#         'Method',
#         related_name='grouping_methods',
#         related_query_name='grouping_methods',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

# class OperationMethod(Standard, Choice):
#     """Method used to operate on an inbound message group.

#     Last updated: 28 April 2021, 3:20 PM
#     """

#     applied = models.DateTimeField(db_index=True)
#     order = models.IntegerField(db_index=True)
#     output_body = models.TextField(
#         null=True,
#         blank=True
#     )

#     inbound_message_group = models.ForeignKey(
#         'InboundMessageGroup',
#         related_name='operation_methods',
#         related_query_name='operation_methods',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     method = models.ForeignKey(
#         'Method',
#         related_name='operation_methods',
#         related_query_name='operation_methods',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

# class Method(Standard, Choice):
#     """Manual or automated (algorithm) method.

#     Last updated: 23 April 2021, 1:49 PM
#     """

#     is_function = models.BooleanField(
#         default=False,
#         db_index=True
#     )
#     title = models.CharField(
#         max_length=200,
#         db_index=True
#     )
#     version = models.CharField(
#         max_length=200,
#         db_index=True
#     )
	
#     tags = models.ManyToManyField(
#         'MethodTag',
#         related_name='methods',
#         related_query_name='methods',
#         blank=True,
#         db_index=True
#     )

#     def __str__(self):
#         return f'({self.title} [{self.id}])'

# class MethodTag(Standard, Choice):
#     """Method tag.

#     Last updated: 26 April 2021, 9:31 PM
#     """
#     pass

# class InboundMessageGroupRelationship(Standard):
#     """Relationship of an inbound message group to model(s).

#     Last updated: 23 April 2021, 2:00 PM
#     """

#     associated = models.DateTimeField(db_index=True)
#     group = models.ForeignKey(
#         'InboundMessageGroup',
#         related_name='inbound_message_group_relationships',
#         related_query_name='inbound_message_group_relationships',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

#     tags = models.ManyToManyField(
#         'InboundMessageGroupRelationshipTag',
#         related_name='inbound_message_group_relationships',
#         related_query_name='inbound_message_group_relationships',
#         db_index=True
#     )
	
#     supplies = models.ManyToManyField(
#         'relationships.Supply',
#         related_name='inbound_message_group_relationships',
#         related_query_name='inbound_message_group_relationships',
#         db_index=True
#     )
#     demands = models.ManyToManyField(
#         'relationships.Demand',
#         related_name='inbound_message_group_relationships',
#         related_query_name='inbound_message_group_relationships',
#         db_index=True
#     )
#     supply_quotes = models.ManyToManyField(
#         'relationships.SupplyQuote',
#         related_name='inbound_message_group_relationships',
#         related_query_name='inbound_message_group_relationships',
#         db_index=True
#     )
#     demand_quotes = models.ManyToManyField(
#         'relationships.DemandQuote',
#         related_name='inbound_message_group_relationships',
#         related_query_name='inbound_message_group_relationships',
#         db_index=True
#     )

# class InboundMessageGroupRelationshipTag(Standard, Choice):
#     """Type of inbound-message-group-to-model relationship.

#     Last updated: 23 April 2021, 2:18 PM
#     """
#     pass

# class TestRunType(Standard, Choice):
#     """Type of test run. A run is a test of a list of message groups against
#     functions and each expected output (i.e., base truths).

#     Last updated: 28 April 2021, 11:14 AM
#     """
#     setting = models.CharField(
#         max_length=2,
#         choices=[
#             ('a', 'Run All Methods on All Message Groups'),
#             ('b', 'Run Base Truth Methods Only')
#         ],
#         db_index=True
#     )
#     methods = models.ManyToManyField(
#         'Method',
#         related_name='test_run_types',
#         related_query_name='test_run_types',
#         blank=True,
#         db_index=True
#     )

# class TestRun(Standard):
#     """A test run - i.e., a test of a list of message groups against functions
#     and each expected output (i.e., base truths).

#     Last updated: 28 April 2021, 11:24 AM
#     """
#     test_run_type = models.ForeignKey(
#         'TestRunType',
#         related_name='test_runs',
#         related_query_name='test_runs',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     ran = models.DateTimeField(db_index=True)

#     def __str__(self):
#         return f'({self.ran} [{self.id}])'

# class TestRunResult(Standard):
#     """Single test run result - i.e., of a test message group against its base
#     truth.

#     Last updated: 28 April 2021, 3:22 AM
#     """
#     test_message_group = models.ForeignKey(
#         'TestMessageGroup',
#         related_name='test_run_results',
#         related_query_name='test_run_results',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
    
#     method = models.ForeignKey(
#         'Method',
#         related_name='test_run_results',
#         related_query_name='test_run_results',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     expected_output	= models.TextField()
#     actual_output = models.TextField()
#     matched = models.BooleanField(db_index=True)
	
#     test_run = models.ForeignKey(
#         'TestRun',
#         related_name='test_run_results',
#         related_query_name='test_run_results',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

#     def __str__(self):
#         return f'({self.test_message_group}, [{self.id}])'