from django.db import models
from common.models import Standard, Choice

class Currency(Choice):
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'