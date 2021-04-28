from django.db import models
from common.models import Standard, Choice, short_text
from django.core.exceptions import ValidationError

class TestMessageGroup(Standard):
    """Message group (to ascertain base truths on). The unit of operation is a
    group of messages.

    Last updated: 27 April 2021, 9:06 PM
    """
    body = models.TextField(db_index=True)

    def __str__(self):
        return f'({short_text(self.body)} [{self.id}])'

class BaseTruth(Standard):
    """Base truth - i.e., what we expect when we run a function over a message.

    Last updated: 26 April 2021, 10:51 AM
    """
    message_group = models.ForeignKey(
        'TestMessageGroup',
        related_name='base_truths',
        related_query_name='base_truths',
        on_delete=models.PROTECT,
        db_index=True
    )
    # method = models.ForeignKey(
    #     'Method',
    #     related_name='base_truths',
    #     related_query_name='base_truths',
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )

    text_output = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    integer_output = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    float_output = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    def clean(self):
        super(BaseTruth, self).clean()

        count = 0
        if self.text_output is not None:
            count += 1

        if self.integer_output is not None:
            count += 1

        if self.float_output is not None:
            count += 1

        # Either 1 of 3 outputs must be set.
        if count != 1:
            raise ValidationError('Either text_output, integer_output, \
                or float_output must be set.')

    def __str__(self):
        return f'({self.message}, {self.function} [{self.id}])'

# class InboundMessageGroup(Standard):
#     """We operate on inbound messages one group at a time. This is a group of
#     inbound messages.

#     Last updated: 23 April 2021, 11:52 AM
#     """

#     is_disabled	= models.BooleanField(db_index=True)
#     grouped = models.DateTimeField(db_index=True)
#     initial_body = models.TextField(db_index=True)

#     twilio_inbound_messages = models.ManyToManyField(
#         'TwilioInboundMessage',
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

#     Last updated: 23 April 2021, 1:36 PM
#     """

#     applied = models.DateTimeField(db_index=True)
#     order = models.IntegerField(db_index=True)
#     output_body = models.TextField(
#         null=True,
#         blank=True,
#         db_index=True
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