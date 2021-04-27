from django.db import models
from common.models import Standard, Choice
from django.core.exceptions import ValidationError

class TestMessageGroup(Standard):
    """Message group (to ascertain base truths on). The unit of operation is a
    group of messages.

    Last updated: 26 April 2021, 10:51 AM
    """
    body = models.TextField(db_index=True)

    def __str__(self):
        return f'({self.body[:50]} [{self.id}])'

class BaseTruth(Standard):
    """Base truth - i.e., what we expect when we run a function over a message.

    Last updated: 26 April 2021, 10:51 AM
    """
    message_group = models.ForeignKey(
        'TestMessageGroup',
        related_name='base_truths',
        related_query_name='base_truths',
        on_delete=models.PROTECT,
        db_index=True
    )
    method = models.ForeignKey(
        'chat.Method',
        related_name='base_truths',
        related_query_name='base_truths',
        on_delete=models.PROTECT,
        db_index=True
    )

    text_output = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    integer_output = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    float_output = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    def clean(self):
        super(BaseTruth, self).clean()

        count = 0
        if self.text_output is not None:
            count += 1

        if self.integer_output is not None:
            count += 1

        if self.float_output is not None:
            count += 1

        # Either 1 of 3 outputs must be set.
        if count != 1:
            raise ValidationError('Either text_output, integer_output, \
                or float_output must be set.')

    def __str__(self):
        return f'({self.message}, {self.function} [{self.id}])'