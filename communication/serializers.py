# from rest_framework import serializers
# from common.models import standard_fieldnames, choice_fieldnames
# from . import models

# class IssueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Issue
#         fields = ['id', 'scheduled', 'description_md', 'outcome_md', 'tags',
#             'status', 'supply', 'demand', 'supply_quote', 'match',
#             'supply_commission', 'demand_commission']

# class IssueTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.IssueTag
#         fields = ['id'] + choice_fieldnames + ['parent']

# class IssueStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.IssueStatus
#         fields = ['id'] + choice_fieldnames + ['parent']

# class ConversationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Conversation
#         fields = ['id'] + standard_fieldnames + ['channel', 'agenda_md',
#             'minutes_md', 'front_conversation_id', 'emails', 'chats', 'voices',
#             'videos', 'issue']

# class ConversationChannelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationChannel
#         fields = ['id'] + choice_fieldnames

# class ConversationEmailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationEmail
#         fields = ['id'] + standard_fieldnames + ['status', 'their_email',
#             'our_email', 'conversation']

# class ConversationEmailStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationEmailStatus
#         fields = ['id'] + choice_fieldnames

# class ConversationChatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationChat
#         fields = ['id'] + standard_fieldnames + ['status', 'their_number',
#             'our_number', 'conversation']

# class ConversationChatStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationChatStatus
#         fields = ['id'] + choice_fieldnames

# class ConversationVoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationVoice
#         fields = ['id'] + standard_fieldnames + ['status', 'their_number',
#             'our_number', 'conversation']

# class ConversationVoiceStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationVoiceStatus
#         fields = ['id'] + choice_fieldnames

# class ConversationVideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationVideo
#         fields = ['id'] + standard_fieldnames + ['status', 'their_number',
#             'our_number', 'conversation']

# class ConversationVideoStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ConversationVideoStatus
#         fields = ['id'] + choice_fieldnames