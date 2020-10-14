from django.contrib import admin
from .models import (Issue, IssueTag, IssueStatus, Conversation,
    ConversationChannel, ConversationEmail, ConversationEmailStatus,
    ConversationChat, ConversationChatStatus, ConversationVoice,
    ConversationVoiceStatus, ConversationVideo, ConversationVideoStatus)

admin.site.register(Issue)
admin.site.register(IssueTag)
admin.site.register(IssueStatus)
admin.site.register(Conversation)
admin.site.register(ConversationChannel)
admin.site.register(ConversationEmail)
admin.site.register(ConversationEmailStatus)
admin.site.register(ConversationChat)
admin.site.register(ConversationChatStatus)
admin.site.register(ConversationVoice)
admin.site.register(ConversationVoiceStatus)
admin.site.register(ConversationVideo)
admin.site.register(ConversationVideoStatus)