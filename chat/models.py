from django.db import models
from django.core.exceptions import ValidationError
from common.models import Standard, Choice, short_text
from chat.libraries import intents, messages

class TwilioOutboundMessage(Standard):
    """Twilio outbound message.

    Last updated: 25 May 2021, 11:53 PM
    """

    context = models.ForeignKey(
        'UserContext',
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
        related_query_name='twilio_outbound_message_from_users',
        on_delete=models.PROTECT,
        db_index=True
    )
    to_user = models.ForeignKey(
        'relationships.User',
        null=True,
        blank=True,
        related_name='twilio_outbound_message_to_users',
        related_query_name='twilio_outbound_message_to_users',
        on_delete=models.PROTECT,
        db_index=True
    )

    from_phone_number = models.ForeignKey(
        'relationships.PhoneNumber',
        null=True,
        blank=True,
        related_name='twilio_outbound_message_from_phone_numbers',
        related_query_name='twilio_outbound_message_from_phone_numbers',
        on_delete=models.PROTECT,
        db_index=True
    )
    to_phone_number = models.ForeignKey(
        'relationships.PhoneNumber',
        null=True,
        blank=True,
        related_name='twilio_outbound_message_to_phone_numbers',
        related_query_name='twilio_outbound_message_to_phone_numbers',
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

    Last updated: 15 May 2021, 2:26 PM
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

    # Associated users
    from_user = models.ForeignKey(
        'relationships.User',
        related_name='twilio_inbound_message_from_users',
        related_query_name='twilio_inbound_message_from_users',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    to_user = models.ForeignKey(
        'relationships.User',
        related_name='twilio_inbound_message_to_users',
        related_query_name='twilio_inbound_message_to_users',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    # Associated phone numbers
    from_phone_number = models.ForeignKey(
        'relationships.PhoneNumber',
        null=True,
        blank=True,
        related_name='twilio_inbound_message_from_phone_numbers',
        related_query_name='twilio_inbound_message_from_phone_numbers',
        on_delete=models.PROTECT,
        db_index=True
    )
    to_phone_number = models.ForeignKey(
        'relationships.PhoneNumber',
        null=True,
        blank=True,
        related_name='twilio_inbound_message_to_phone_numbers',
        related_query_name='twilio_inbound_message_to_phone_numbers',
        on_delete=models.PROTECT,
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

class MessageDataset(Standard):
    """A set of data extracted in-context for a message. A context is a unique
    intent-message pair for an incoming Twilio message.

    Last updated: 24 May 2021, 10:08 PM
    """
    intent_key = models.CharField(
        max_length=200,
        choices=intents.choices,
        db_index=True
    )
    message_key = models.CharField(
        max_length=200,
        choices=messages.choices,
        db_index=True
    )
    message = models.ForeignKey(
        'TwilioInboundMessage',
        related_name='message_datasets',
        related_query_name='message_datasets',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.intent_key}, {self.message_key}, {self.message} [{self.id}])'

    class Meta:
        unique_together = ('intent_key', 'message_key', 'message')

class MessageDataString(Standard):
    """String extracted from an incoming Twilio message in its context

    Last updated: 26 May 2021, 11:45 PM
    """
    dataset = models.ForeignKey(
        'MessageDataset',
        related_name='strings',
        related_query_name='strings',
        on_delete=models.PROTECT,
        db_index=True
    )
    value = models.CharField(
        max_length=200,
        db_index=True
    )
    is_valid = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

class MessageDataFloat(Standard):
    """Float extracted from an incoming Twilio message in its context

    Last updated: 26 May 2021, 11:45 PM
    """
    dataset = models.ForeignKey(
        'MessageDataset',
        related_name='floats',
        related_query_name='floats',
        on_delete=models.PROTECT,
        db_index=True
    )
    value = models.FloatField(db_index=True)
    is_valid = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

class MessageDataBoolean(Standard):
    """Boolean extracted from an incoming Twilio message in its context

    Last updated: 26 May 2021, 11:45 PM
    """
    dataset = models.ForeignKey(
        'MessageDataset',
        related_name='booleans',
        related_query_name='booleans',
        on_delete=models.PROTECT,
        db_index=True
    )
    value = models.BooleanField(db_index=True)
    is_valid = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )

class UserContext(Standard):
    """User context

    Last updated: 25 May 2021, 12:06 PM
    """

    # Only 1 active context at a time, the others should either be done, paused
    # or expired
    started = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    done = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    paused = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    expired = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        'relationships.User',
        null=True,
        blank=True,
        related_name='user_contexts',
        related_query_name='user_contexts',
        on_delete=models.PROTECT,
        db_index=True
    )
    intent_key = models.CharField(
        max_length=200,
        choices=intents.choices,
        db_index=True
    )
    message_key = models.CharField(
        max_length=200,
        choices=messages.choices,
        db_index=True
    )

    def __str__(self):
        return f'({self.user}, {self.intent_key}, {self.message_key} [{self.id}])'

    def clean(self):
        super(UserContext, self).clean()

        # Get count of active contexts
        a_count = UserContext.objects.filter(
            user=self.user,
            done__isnull=True,
            paused__isnull=True,
            expired__isnull=True
        ).count()

        if self.started is not None and (self.done is None and \
            self.paused is None and self.expired is None) and a_count > 0:
            # This context is active and there's at least 1 other active context
            raise ValidationError('There can be only 1 active context for a \
                user at one time.')

    class Meta:
        unique_together = ['user', 'intent_key', 'message_key']