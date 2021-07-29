from django.db import models
from common.models import Standard

class Event(Standard):
    """Event

    Last updated: 27 July 2021, 2:07 PM
    """
    requested = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    responded = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    response_code = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    # Note: we store user.key instead of user.id in this field because of the
    # 5 min-length requirement of Amplitude.
    user_id = models.CharField(
        max_length=200,
        db_index=True
    )
    device_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,        
        db_index=True
    )
    event_type = models.CharField(
        max_length=200,
        db_index=True
    )
    time_dt = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    time = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    app_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    platform = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    os_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    os_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    device_brand = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    device_manufacturer = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    device_model = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    carrier = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    region = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    city = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    dma = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    language = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    price = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    quantity = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    revenue = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    product_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    revenue_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    location_lat = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    location_lng = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    ip = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    idfa = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    idfv = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    adid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    android_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    event_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    session_id = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    insert_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return \
        f'({self.user_id}, {self.event_type}, {self.response_code} [{self.id}])'

class EventProperty(Standard):
    """Event property

    Last updated: 27 July 2021, 2:07 PM
    """
    key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    value = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    event = models.ForeignKey(
        'Event',
        related_name='event_properties',
        related_query_name='event_properties',
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Event property'
        verbose_name_plural = 'Event properties'

class UserProperty(Standard):
    """User property

    Last updated: 27 July 2021, 2:07 PM
    """
    key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    value = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        'relationships.User',
        related_name='user_properties',
        related_query_name='user_properties',
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'User property'
        verbose_name_plural = 'User properties'

class Session(Standard):
    """Session

    Last updated: 27 July 2021, 2:07 PM
    """
    started = models.DateTimeField(db_index=True)
    session_id = models.BigIntegerField(db_index=True)
    last_activity = models.DateTimeField(
        max_length=200,
        db_index=True
    )

    user = models.ForeignKey(
        'relationships.user',
        related_name='sessions',
        related_query_name='sessions',
        on_delete=models.PROTECT,
        db_index=True
    )