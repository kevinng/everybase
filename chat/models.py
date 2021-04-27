from django.db import models
from common.models import Standard, Choice, short_text

class MessageTemplate(Standard):
    """Message template.

    Last updated: 23 April 2021, 10:00 AM
    """

    programmatic_key = models.CharField(
        max_length=200,
        db_index=True
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True
    )
    internal_title = models.CharField(
        max_length=200,
        db_index=True
    )
    notes = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
    body = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.internal_title} [{self.id}])'

class TwilioOutboundMessage(Standard):
    """Twilio outbound message.

    Last updated: 23 April 2021, 9:24 AM
    """

    message_template = models.ForeignKey(
        'MessageTemplate',
        related_name='twilio_outbound_messages',
        related_query_name='twilio_outbound_messages',
        on_delete=models.PROTECT,
        db_index=True
    )
    date_created = models.DateField(
        null=True,
        blank=True,
        db_index=True
    )
    date_sent = models.DateField(
        null=True,
        blank=True,
        db_index=True
    )
    direction = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    account_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    message_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    from_str = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_str = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    body = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
    uri = models.URLField(
        null=True,
        blank=True,
        db_index=True
    )
    error_message = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    error_code = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    api_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
	
    from_user = models.ForeignKey(
        'relationships.User',
        null=True,
        blank=True,
        related_name='twilio_outbound_message_from_users',
        related_query_name='twilio_outbound_from_users',
        on_delete=models.PROTECT,
        db_index=True
    )
    to_user = models.ForeignKey(
        'relationships.User',
        null=True,
        blank=True,
        related_name='twilio_outbound_message_to_users',
        related_query_name='twilio_outbound_to_users',
        on_delete=models.PROTECT,
        db_index=True
    )
	
    twilml_response_to = models.ForeignKey(
        'TwilioInboundMessage',
        null=True,
        blank=True,
        related_name='twilio_outbound_message_responses',
        related_query_name='twilio_outbound_message_responses',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.to_str}, {short_text(self.body)} [{self.id}])'

class TwilioStatusCallback(Standard):
    """Twilio status callback.

    Last updated: 27 April 2021, 5:10 PM
    """

    from_str = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_str = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    account_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    api_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    channel_to_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    channel_install_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    channel_status_message = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    channel_prefix = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    message_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    message_status = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    sms_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    sms_status = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    error_code = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    event_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
	
    message = models.ForeignKey(
        'TwilioOutboundMessage',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.to_str} [{self.id}])'

class TwilioStatusCallbackLogEntry(Standard):
    """Twilio status callback log entry. 

    Last updated: 27 April 2021, 5:10 PM
    """

    payload = models.TextField(db_index=True)
    callback = models.ForeignKey(
        'TwilioStatusCallback',
        related_name='log_entries',
        related_query_name='log_entries',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({short_text(self.payload)} [{self.id}])'

    class Meta:
        verbose_name = 'Twilio Status Callback Log Entry'
        verbose_name_plural = 'Twilio Status Callback Log Entries'

class TwilioInboundMessage(Standard):
    """Twilio inbound message.

    Last updated: 23 April 2021, 10:55 AM
    """

    # Request parameters
    api_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    message_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    sms_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    sms_message_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    account_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    message_service_sid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    from_str = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_str = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    body = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
    num_media = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    num_segments = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    # Geographic data-related parameters
    from_city = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    from_state = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    from_zip = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    from_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_city = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_state = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_zip = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    to_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    # WhatsApp-specific parameters
    profile_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    wa_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    forwarded = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    frequently_forwarded = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    # WhatsApp location-sharing parameters
    latitude = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    longitude = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    label = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.from_str}, {short_text(self.body)} [{self.id}])'    

class TwilioInboundMessageMedia(Standard):
    """Twilio inbound message media.

    Last updated: 23 April 2021, 11:19 AM
    """

    content_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
	
    message = models.ForeignKey(
        'TwilioInboundMessage',
        related_name='medias',
        related_query_name='medias',
        on_delete=models.PROTECT,
        db_index=True
    )

class TwilioInboundMessageLogEntry(Standard):
    """Twilio inbound message log entry.

    Last updated: 23 April 2021, 11:47 AM
    """

    payload = models.TextField(db_index=True)
    message = models.ForeignKey(
        'TwilioInboundMessage',
        related_name='log_entries',
        related_query_name='log_entries',
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Twilio Inbound Message Log Entry'
        verbose_name_plural = 'Twilio Inbound Message Log Entries'

    def __str__(self):
        return f'({self.message} [{self.id}])'

class InboundMessageGroup(Standard):
    """We operate on inbound messages one group at a time. This is a group of
    inbound messages.

    Last updated: 23 April 2021, 11:52 AM
    """

    is_disabled	= models.BooleanField(db_index=True)
    grouped = models.DateTimeField(db_index=True)
    initial_body = models.TextField(db_index=True)

    twilio_inbound_messages = models.ManyToManyField(
        'TwilioInboundMessage',
        related_name='inbound_message_groups',
        related_query_name='inbound_message_groups',
        db_index=True
    )

class GroupingMethod(Standard, Choice):
    """Method used to group a group of Twilio inbound messages.

    Last updated: 23 April 2021, 1:13 PM
    """

    applied = models.DateTimeField(db_index=True)
    order = models.IntegerField(db_index=True)
	
    inbound_message_group = models.ForeignKey(
        'InboundMessageGroup',
        related_name='grouping_methods',
        related_query_name='grouping_methods',
        on_delete=models.PROTECT,
        db_index=True
    )
    method = models.ForeignKey(
        'Method',
        related_name='grouping_methods',
        related_query_name='grouping_methods',
        on_delete=models.PROTECT,
        db_index=True
    )

class OperationMethod(Standard, Choice):
    """Method used to operate on an inbound message group.

    Last updated: 23 April 2021, 1:36 PM
    """

    applied = models.DateTimeField(db_index=True)
    order = models.IntegerField(db_index=True)
    output_body = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )

    inbound_message_group = models.ForeignKey(
        'InboundMessageGroup',
        related_name='operation_methods',
        related_query_name='operation_methods',
        on_delete=models.PROTECT,
        db_index=True
    )
    method = models.ForeignKey(
        'Method',
        related_name='operation_methods',
        related_query_name='operation_methods',
        on_delete=models.PROTECT,
        db_index=True
    )

class Method(Standard, Choice):
    """Manual or automated (algorithm) method.

    Last updated: 23 April 2021, 1:49 PM
    """

    title = models.CharField(
        max_length=200,
        db_index=True
    )
    version = models.CharField(
        max_length=200,
        db_index=True
    )
	
    tags = models.ManyToManyField(
        'MethodTag',
        related_name='methods',
        related_query_name='methods',
        blank=True,
        db_index=True
    )

class MethodTag(Standard, Choice):
    """Method tag.

    Last updated: 26 April 2021, 9:31 PM
    """
    pass

class InboundMessageGroupRelationship(Standard):
    """Relationship of an inbound message group to model(s).

    Last updated: 23 April 2021, 2:00 PM
    """

    associated = models.DateTimeField(db_index=True)
    group = models.ForeignKey(
        'InboundMessageGroup',
        related_name='inbound_message_group_relationships',
        related_query_name='inbound_message_group_relationships',
        on_delete=models.PROTECT,
        db_index=True
    )

    tags = models.ManyToManyField(
        'InboundMessageGroupRelationshipTag',
        related_name='inbound_message_group_relationships',
        related_query_name='inbound_message_group_relationships',
        db_index=True
    )
	
    supplies = models.ManyToManyField(
        'relationships.Supply',
        related_name='inbound_message_group_relationships',
        related_query_name='inbound_message_group_relationships',
        db_index=True
    )
    demands = models.ManyToManyField(
        'relationships.Demand',
        related_name='inbound_message_group_relationships',
        related_query_name='inbound_message_group_relationships',
        db_index=True
    )
    supply_quotes = models.ManyToManyField(
        'relationships.SupplyQuote',
        related_name='inbound_message_group_relationships',
        related_query_name='inbound_message_group_relationships',
        db_index=True
    )
    demand_quotes = models.ManyToManyField(
        'relationships.DemandQuote',
        related_name='inbound_message_group_relationships',
        related_query_name='inbound_message_group_relationships',
        db_index=True
    )

class InboundMessageGroupRelationshipTag(Standard, Choice):
    """Type of inbound-message-group-to-model relationship.

    Last updated: 23 April 2021, 2:18 PM
    """
    pass