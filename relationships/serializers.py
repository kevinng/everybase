from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import relationship_fieldnames
from . import models

class PersonLinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonLinkType
        fields = ['id'] + choice_fieldnames