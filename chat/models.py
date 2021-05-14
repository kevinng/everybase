from django.db import models
from common.models import Standard, Choice, short_text

class MessageTemplate(Standard, Choice):
    """Message template.

    Last updated: 11 May 2021, 9:08 PM
    """

    chat_context_type = models.ForeignKey(
        'ChatContextType',
        related_name='message_templates',
        related_query_name='message_templates',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

class TwilioOutboundMessage(Standard):
    """Twilio outbound message.

    Last updated: 28 April 2021, 3:31 PM
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
        blank=True
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

    Last updated: 28 April 2021, 3:32 PM
    """

    payload = models.TextField(db_index=True)
    callback = models.ForeignKey(
        'TwilioStatusCallback',
        related_name='log_entries',
        related_query_name='log_entries',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'({short_text(self.payload)} [{self.id}])'

    class Meta:
        verbose_name = 'Twilio Status Callback Log Entry'
        verbose_name_plural = 'Twilio Status Callback Log Entries'

class TwilioInboundMessage(Standard):
    """Twilio inbound message.

    Last updated: 28 April 2021, 3:33 PM
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
    sms_status = models.CharField(
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
        blank=True
    )
    num_media = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    num_segment = models.CharField(
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

class UserChatContext(Standard):
    """Tracks chat contexts of users.

    Last updated: 23 April 2021, 11:47 AM
    """

    started = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
    )
    stopped = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'relationships.User',
        related_name='user_chat_contexts',
        related_query_name='user_chat_contexts',
        on_delete=models.PROTECT,
        db_index=True
    )
    chat_context_type = models.ForeignKey(
        'ChatContextType',
        related_name='user_chat_contexts',
        related_query_name='user_chat_contexts',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.message} [{self.id}])'

class ChatContextType(Choice):
    """Chat context types.

    Last updated: 11 May 2021, 9:20 PM
    """
    pass