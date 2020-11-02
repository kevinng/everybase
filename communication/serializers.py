from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from . import models

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = ['id', 'scheduled', 'description_md', 'outcome_md', 'tags',
            'status', 'supply', 'demand', 'supply_quote', 'match',
            'supply_commission', 'demand_commission']

class IssueTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IssueTag
        fields = ['id'] + choice_fieldnames + ['parent']

class IssueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IssueStatus
        fields = ['id'] + choice_fieldnames + ['parent']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conversation
        fields = ['id'] + standard_fieldnames + ['channel', 'agenda_md',
            'minutes_md', 'front_conversation_id', 'emails', 'chats', 'voices',
            'videos', 'issue']