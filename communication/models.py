from django.db import models
from common.models import Standard, Choice, ParentChildrenChoice
from relationships.models import Email, PhoneNumber

# --- Start: Abstract ---

# Helper function to declare foreign key relationships.
fk = lambda klass, name: models.ForeignKey(
        klass,
        on_delete=models.PROTECT,
        related_name=name,
        related_query_name=name
    )

# Helper function to declare many-to-many relationships.
m2m = lambda klass, name: models.ManyToManyField(
        klass,
        related_name=name,
        related_query_name=name
    )

# --- End: Abstract ---

# --- Start: Issue classes ---

class Issue(Standard):
    scheduled = models.DateTimeField(null=True, default=None)
    description_md = models.TextField()
    outcome_md = models.TextField()

    tags = m2m('IssueTag', 'issues')
    status = fk('IssueStatus', 'issues')

    # At least one of the following source must be set.
    supply = fk('leads.Supply', 'issues')
    demand = fk('leads.Demand', 'issues')
    supply_quote = fk('leads.SupplyQuote', 'issues')
    match = fk('leads.Match', 'issues')
    supply_commission = fk('leads.SupplyCommission', 'issues')
    demand_commission = fk('leads.DemandCommission', 'issues')

class IssueTag(ParentChildrenChoice):
    pass

class IssueStatus(ParentChildrenChoice):
    pass

# --- End: Issue classes ---

# --- Start: Conversation classes ---

class Conversation(Standard):
    channel = fk('ConversationChannel', 'conversations')

    agenda_md = models.TextField()
    minutes_md = models.TextField()

    front_conversation_id = models.CharField(max_length=100)

    # At least one of the following channels must be set.
    emails = fk('ConversationEmail', 'conversations')
    chats = fk('ConversationChat', 'conversations')
    voices = fk('ConversationVoice', 'conversations')
    videos = fk('ConversationVideo', 'conversations')

    issue = fk('Issue', 'conversations')

class ConversationChannel(Choice):
    pass

class ConversationEmail(Standard):
    status = fk('ConversationEmailStatus', 'conversation_emails')
    to_email = fk('relationships.Email', 'conversation_email_tos')
    from_email = fk('relationships.Email', 'conversation_email_froms')
    conversation = fk('Conversation', 'conversation_emails')

class ConversationEmailStatus(Choice):
    pass

class ConversationChat(Standard):
    status = fk('ConversationChatStatus', 'conversation_chats')
    to_number = fk('relationships.PhoneNumber', 'conversation_chat_tos')
    from_number = fk('relationships.PhoneNumber', 'conversation_chat_froms')
    conversation = fk('Conversation', 'conversation_chats')

class ConversationChatStatus(Choice):
    pass

class ConversationVoice(Standard):
    status = fk('ConversationVoiceStatus', 'conversation_voices')
    to_number = fk('relationships.PhoneNumber', 'conversation_voice_tos')
    from_number = fk('relationships.PhoneNumber', 'conversation_voice_froms')
    conversation = fk('Conversation', 'conversation_voices')

class ConversationVoiceStatus(Choice):
    pass

class ConversationVideo(models.Model):
    status = fk('ConversationVideoStatus', 'conversation_videos')
    to_number = fk('relationships.PhoneNumber', 'conversation_video_tos')
    from_number = fk('relationships.PhoneNumber', 'conversation_video_froms')
    conversation = fk('Conversation', 'conversation_videos')

class ConversationVideoStatus(Choice):
    pass

# --- End: Conversation-related classes ---