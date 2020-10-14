from django.db import models
from common.models import Standard, Choice, ParentChildrenChoice
from relationships.models import Email, PhoneNumber

# --- Start: Helper lambda for model field declarations ---

# Foreign key
fk = lambda klass, name=None, verbose_name=None, null=False: models.ForeignKey(
    klass,
    on_delete=models.PROTECT,
    related_name=name,
    related_query_name=name,
    verbose_name=verbose_name,
    null=null,
    blank=null
)

# Many-to-many
m2m = lambda klass, name, blank=False: models.ManyToManyField(
    klass,
    related_name=name,
    related_query_name=name,
    blank=blank
)

# Many-to-many through
m2mt = lambda klass, thru, f1, f2, name: models.ManyToManyField(
    klass,
    through=thru,
    through_fields=(f1, f2),
    related_name=name,
    related_query_name=name
)

# Text
tf = lambda verbose_name=None, null=False: models.TextField(
    verbose_name=verbose_name, null=null, blank=null)

# Char
cf = lambda verbose_name=None, null=False: models.CharField(
    verbose_name=verbose_name, max_length=100, null=null, blank=null)

# Float
ff = lambda verbose_name=None, null=False: models.FloatField(
    verbose_name=verbose_name, null=null, blank=null)

# Datetime
dtf = lambda verbose_name=None, null=False, default=None: models.DateTimeField(
    null=null, blank=null, default=default)

# --- End: Helper lambda for model field declarations ---


# # --- Start: Abstract ---

# # Helper function to declare foreign key relationships.
# fk = lambda klass, name: models.ForeignKey(
#         klass,
#         on_delete=models.PROTECT,
#         related_name=name,
#         related_query_name=name
#     )

# # Helper function to declare many-to-many relationships.
# m2m = lambda klass, name: models.ManyToManyField(
#         klass,
#         related_name=name,
#         related_query_name=name
#     )

# # --- End: Abstract ---

# --- Start: Issue classes ---

class Issue(Standard):
    scheduled = dtf()
    description_md = tf('Description in Markdown', null=True)
    outcome_md = tf('Outcome in Markdown', null=True)

    tags = m2m('IssueTag', 'issues', blank=True)
    status = fk('IssueStatus', 'issues')

    # At least one of the following source must be set.
    supply = fk('leads.Supply', 'issues', null=True)
    demand = fk('leads.Demand', 'issues', null=True)
    supply_quote = fk('leads.SupplyQuote', 'issues', null=True)
    match = fk('leads.Match', 'issues', null=True)
    supply_commission = fk('leads.SupplyCommission', 'issues', null=True)
    demand_commission = fk('leads.DemandCommission', 'issues', null=True)

class IssueTag(ParentChildrenChoice):
    pass

class IssueStatus(ParentChildrenChoice):
    pass

# --- End: Issue classes ---

# --- Start: Conversation classes ---

class Conversation(Standard):
    channel = fk('ConversationChannel', 'conversations')

    agenda_md = tf('Agenda in Markdown', null=True)
    minutes_md = tf('Minutes in Markdown', null=True)

    front_conversation_id = cf('Front conversation ID', null=True)

    # At least one of the following channels must be set.
    emails = fk('ConversationEmail', 'conversations', null=True)
    chats = fk('ConversationChat', 'conversations', null=True)
    voices = fk('ConversationVoice', 'conversations', null=True)
    videos = fk('ConversationVideo', 'conversations', null=True)

    issue = fk('Issue', 'conversations', null=True)

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