from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import GmassCampaignResult, GmassCampaign

class GmassCampaignResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GmassCampaignResult
        fields = ['id'] + standard_fieldnames + ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied',
            'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
            'bounce_reason', 'gmail_response', 'email', 'gmass_campaign']

class GmassCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = GmassCampaign
        fields = ['id'] + standard_fieldnames + ['campaign_id', 'sent',
            'subject', 'spreadsheet']