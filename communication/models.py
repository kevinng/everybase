from django.db import models
from common.models import fk, m2m, tf, cf, dtf
from common.models import Standard, Choice
from relationships.models import Email, PhoneNumber

# --- Start: Issue classes ---

class Issue(Standard):
    scheduled = dtf(null=True)
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

class IssueTag(Choice):
    parent = fk('self', 'children', null=True)

class IssueStatus(Choice):
    parent = fk('self', 'children', null=True)
    class Meta:
        verbose_name = 'Issue status'
        verbose_name_plural = 'Issue statuses'

# --- End: Issue classes ---

# --- Start: Conversation classes ---

class Conversation(Standard):
    channel = fk('ConversationChannel', 'conversations')

    agenda_md = tf('Agenda in Markdown', null=True)
    minutes_md = tf('Minutes in Markdown', null=True)

    front_conversation_id = cf('Front conversation ID', null=True)

    # One and only one of the following conversations must be set.
    emails = fk('ConversationEmail', 'conversations', null=True)
    chats = fk('ConversationChat', 'conversations', null=True)
    voices = fk('ConversationVoice', 'conversations', null=True)
    videos = fk('ConversationVideo', 'conversations', null=True)

    issue = fk('Issue', 'conversations')

    def __str__(self):

        if self.agenda_md is None or len(self.agenda_md) > 0:
            top_len = 20
            agenda_top = self.agenda_md[0:top_len]

            if len(self.agenda_md) > top_len:
                agenda_top = agenda_top + '...'
        else:
            agenda_top = ''

        id_str = self.id
        if self.front_conversation_id != None:
            id_str = id_str + ', Front: ' + self.front_conversation_id[0:4]

        return '%s (%s)' % (agenda_top, id_str)

class ConversationChannel(Choice):
    pass

class ConversationEmail(Standard):
    status = fk('ConversationEmailStatus', 'conversation_emails')
    to_email = fk('relationships.Email', 'conversation_email_tos')
    from_email = fk('relationships.Email', 'conversation_email_froms')
    conversation = fk('Conversation', 'conversation_emails')

class ConversationEmailStatus(Choice):
    class Meta:
        verbose_name = 'Conversation email status'
        verbose_name_plural = 'Conversation email statuses'

class ConversationChat(Standard):
    """
    Details for a conversation whose channel is chat.
    """
    status = fk('ConversationChatStatus', 'conversation_chats')
    their_number = fk('relationships.PhoneNumber',
        'conversation_chat_their_numbers')
    our_number = fk('relationships.PhoneNumber',
        'conversation_chat_our_numbers')
    conversation = fk('Conversation', 'conversation_chats')

class ConversationChatStatus(Choice):
    class Meta:
        verbose_name = 'Conversation chat status'
        verbose_name_plural = 'Conversation chat statuses'

class ConversationVoice(Standard):
    status = fk('ConversationVoiceStatus', 'conversation_voices')
    to_number = fk('relationships.PhoneNumber', 'conversation_voice_tos')
    from_number = fk('relationships.PhoneNumber', 'conversation_voice_froms')
    conversation = fk('Conversation', 'conversation_voices')

class ConversationVoiceStatus(Choice):
    class Meta:
        verbose_name = 'Conversation voice status'
        verbose_name_plural = 'Conversation voice statuses'

class ConversationVideo(models.Model):
    status = fk('ConversationVideoStatus', 'conversation_videos')
    to_number = fk('relationships.PhoneNumber', 'conversation_video_tos')
    from_number = fk('relationships.PhoneNumber', 'conversation_video_froms')
    conversation = fk('Conversation', 'conversation_videos')

class ConversationVideoStatus(Choice):
    class Meta:
        verbose_name = 'Conversation video status'
        verbose_name_plural = 'Conversation video statuses'

# --- End: Conversation classes ---