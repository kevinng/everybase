from django.db import models
from common.models import Standard, Choice, short_text
from relationships.models import Email, PhoneNumber

# --- Start: Issue classes ---

class Issue(Standard):
    scheduled = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    description_md = models.TextField(
        verbose_name='Description in Markdown',
        null=True,
        blank=True
    )
    outcome_md = models.TextField(
        verbose_name='Outcome in Markdown',
        null=True,
        blank=True
    )

    tags = models.ManyToManyField(
        'IssueTag',
        related_name='issues',
        related_query_name='issues',
        blank=True,
        db_index=True
    )
    status = models.ForeignKey(
        'IssueStatus',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=False,
        blank=False,
        db_index=True
    )

    # At least one of the following source must be set.
    supply = models.ForeignKey(
        'leads.Supply',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=True,
        blank=True,
        db_index=True
    )
    demand = models.ForeignKey(
        'leads.Demand',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=True,
        blank=True,
        db_index=True
    )
    supply_quote = models.ForeignKey(
        'leads.SupplyQuote',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=True,
        blank=True,
        db_index=True
    )
    match = models.ForeignKey(
        'leads.Match',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=True,
        blank=True,
        db_index=True
    )
    supply_commission = models.ForeignKey(
        'leads.SupplyCommission',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=True,
        blank=True,
        db_index=True
    )
    demand_commission = models.ForeignKey(
        'leads.DemandCommission',
        on_delete=models.PROTECT,
        related_name='issues',
        related_query_name='issues',
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({short_text(self.description_md)} [{self.id}])'

class IssueTag(Choice):
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        related_query_name='children',
        null=True,
        blank=True,
        db_index=True
    )

class IssueStatus(Choice):
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        related_query_name='children',
        null=True,
        blank=True,
        db_index=True
    )
    class Meta:
        verbose_name = 'Issue status'
        verbose_name_plural = 'Issue statuses'

# --- End: Issue classes ---

# --- Start: Conversation classes ---

class Conversation(Standard):
    channel = models.ForeignKey(
        'ConversationChannel',
        on_delete=models.PROTECT,
        related_name='conversations',
        related_query_name='conversations',
        verbose_name=None,
        null=False,
        blank=False,
        db_index=True
    )

    agenda_md = models.TextField(
        verbose_name='Agenda in Markdown',
        null=True,
        blank=True
    )
    minutes_md = models.TextField(
        verbose_name='Minutes in Markdown',
        null=True,
        blank=True
    )

    front_conversation_id = models.CharField(
        verbose_name='Front conversation ID',
        max_length=100,
        null=True,
        blank=True, 
        db_index=True
    )

    # One and only one of the following conversations must be set.
    emails = models.ForeignKey(
        'ConversationEmail',
        on_delete=models.PROTECT,
        related_name='conversations',
        related_query_name='conversations',
        null=True,
        blank=True,
        db_index=True
    )
    chats = models.ForeignKey(
        'ConversationChat',
        on_delete=models.PROTECT,
        related_name='conversations',
        related_query_name='conversations',
        null=True,
        blank=True,
        db_index=True
    )
    voices = models.ForeignKey(
        'ConversationVoice',
        on_delete=models.PROTECT,
        related_name='conversations',
        related_query_name='conversations',
        null=True,
        blank=True,
        db_index=True
    )
    videos = models.ForeignKey(
        'ConversationVideo',
        on_delete=models.PROTECT,
        related_name='conversations',
        related_query_name='conversations',
        null=True,
        blank=True,
        db_index=True
    )

    issue = models.ForeignKey(
        'Issue',
        on_delete=models.PROTECT,
        related_name='conversations',
        related_query_name='conversations',
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'({short_text(self.agenda_md)} [{self.id}])'

class ConversationChannel(Choice):
    pass

class ConversationEmail(Standard):
    status = models.ForeignKey(
        'ConversationEmailStatus',
        on_delete=models.PROTECT,
        related_name='conversation_emails',
        related_query_name='conversation_emails',
        null=False,
        blank=False,
        db_index=True
    )
    their_email = models.ForeignKey(
        'relationships.Email',
        on_delete=models.PROTECT,
        related_name='conversation_email_their_emails',
        related_query_name='conversation_email_their_emails',
        null=False,
        blank=False,
        db_index=True
    )
    our_email = models.ForeignKey(
        'relationships.Email',
        on_delete=models.PROTECT,
        related_name='conversation_email_our_emails',
        related_query_name='conversation_email_our_emails',
        null=False,
        blank=False,
        db_index=True
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.PROTECT,
        related_name='conversation_emails',
        related_query_name='conversation_emails',
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'({self.their_email}, {self.our_email} [{self.id}])'

class ConversationEmailStatus(Choice):
    class Meta:
        verbose_name = 'Conversation email status'
        verbose_name_plural = 'Conversation email statuses'

class ConversationChat(Standard):
    """
    Details for a conversation whose channel is chat.
    """
    status = models.ForeignKey(
        'ConversationChatStatus',
        on_delete=models.PROTECT,
        related_name='conversation_chats',
        related_query_name='conversation_chats',
        null=False,
        blank=False,
        db_index=True
    )
    their_number = models.ForeignKey(
        'relationships.PhoneNumber',
        on_delete=models.PROTECT,
        related_name='conversation_chat_their_numbers',
        related_query_name='conversation_chat_their_numbers',
        null=False,
        blank=False,
        db_index=True
    )
    our_number = models.ForeignKey(
        'relationships.PhoneNumber',
        on_delete=models.PROTECT,
        related_name='conversation_chat_our_numbers',
        related_query_name='conversation_chat_our_numbers',
        null=False,
        blank=False,
        db_index=True
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.PROTECT,
        related_name='conversation_chats',
        related_query_name='conversation_chats',
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'({self.their_number}, {self.our_number} [{self.id}])'

class ConversationChatStatus(Choice):
    class Meta:
        verbose_name = 'Conversation chat status'
        verbose_name_plural = 'Conversation chat statuses'

class ConversationVoice(Standard):
    status = models.ForeignKey(
        'ConversationVoiceStatus',
        on_delete=models.PROTECT,
        related_name='conversation_voices',
        related_query_name='conversation_voices',
        null=False,
        blank=False,
        db_index=True
    )
    their_number = models.ForeignKey(
        'relationships.PhoneNumber',
        on_delete=models.PROTECT,
        related_name='conversation_voice_their_numbers',
        related_query_name='conversation_voice_their_numbers',
        null=False,
        blank=False,
        db_index=True
    )
    our_number = models.ForeignKey(
        'relationships.PhoneNumber',
        on_delete=models.PROTECT,
        related_name='conversation_voice_our_numbers',
        related_query_name='conversation_voice_our_numbers',
        null=False,
        blank=False,
        db_index=True
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.PROTECT,
        related_name='conversation_voices',
        related_query_name='conversation_voices',
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'({self.their_number}, {self.our_number} [{self.id}])'

class ConversationVoiceStatus(Choice):
    class Meta:
        verbose_name = 'Conversation voice status'
        verbose_name_plural = 'Conversation voice statuses'

class ConversationVideo(Standard):
    status = models.ForeignKey(
        'ConversationVideoStatus',
        on_delete=models.PROTECT,
        related_name='conversation_videos',
        related_query_name='conversation_videos',
        null=False,
        blank=False,
        db_index=True
    )
    their_number = models.ForeignKey(
        'relationships.PhoneNumber',
        on_delete=models.PROTECT,
        related_name='conversation_video_their_numbers',
        related_query_name='conversation_video_their_numbers',
        null=False,
        blank=False,
        db_index=True
    )
    our_number = models.ForeignKey(
        'relationships.PhoneNumber',
        on_delete=models.PROTECT,
        related_name='conversation_video_our_numbers',
        related_query_name='conversation_video_our_numbers',
        null=False,
        blank=False,
        db_index=True
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.PROTECT,
        related_name='conversation_videos',
        related_query_name='conversation_videos',
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'({self.their_number}, {self.our_number} [{self.id}])'

class ConversationVideoStatus(Choice):
    class Meta:
        verbose_name = 'Conversation video status'
        verbose_name_plural = 'Conversation video statuses'

# --- End: Conversation classes ---