from django.db import models
from common.utilities.diff_now import diff_now
from common.utilities.diff_now_desc import diff_now_desc
from common.utilities.diff_now_in_days import diff_now_in_days

# --- Start: Helper functions ---

def short_text(text, top_length=20, blank='-', backward=False):
    if text is None or len(text) == 0:
        return blank

    if backward == False:
        details_top = text[0:top_length]
    else:
        details_top = text[-top_length:]

    if len(text) > top_length and backward == False:
        details_top = details_top + '...'
    elif len(text) > top_length and backward == True:
        details_top = '...' + details_top

    return details_top

# --- End: Helper functions ---

# --- Start: Abstract models ---

standard_fieldnames = ['created', 'updated', 'deleted']
class Standard(models.Model):
    """
    Abstract model with standard fields.
    """
    created = models.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True,
        db_index=True
    )
    updated = models.DateTimeField(
        null=True,
        blank=True,
        auto_now=True,
        db_index=True
    )
    deleted = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )

    def age(self):
        return diff_now(self.created)

    def age_desc(self):
        return diff_now_desc(self.created)

    def age_desc_wo_ago(self):
        return self.age_desc().split()[0]

    def age_days(self):
        return diff_now_in_days(self.created)

    class Meta:
        abstract = True

choice_fieldnames = ['name', 'description', 'programmatic_key',
    'programmatic_details']
class Choice(models.Model):
    """
    Abstract model for a choice model.
    """
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True
    )
    description = models.TextField(
        default=None,
        null=True,
        blank=True
    )

    programmatic_key = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )
    programmatic_details = models.TextField(
        verbose_name='Programmatic details',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.id is not None:
            return '(%s [%d])' % (self.name, self.id)
        
        return str(super(Choice, self))

    class Meta:
        abstract = True

class LowerCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCaseCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class LowerCaseEmailField(models.EmailField):
    def __init__(self, *args, **kwargs):
        super(LowerCaseEmailField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

# --- End: Abstract models ---

# --- Start: Common models ---

class Country(Choice):
    cc_tld = models.CharField(
        verbose_name='CC TLD',
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

    source_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    country_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_index=True
    )
    dial_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_index=True
    )
    flag_url = models.URLField(
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.name} [{self.id}]'

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class State(Choice):
    china_province_name_cn = models.CharField(
        'China province name in Chinese',
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'Country',
        on_delete=models.PROTECT,
        related_name='states',
        related_query_name='states',
        null=False,
        blank=False,
        db_index=True
    )

class Language(Choice):
    pass

# --- End: Common models ---

# --- Start: Other models ---

class ImportJob(Standard):
    status = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=[
            ('started', 'Started'),
            ('succeeded', 'Succeeded'),
            ('failed', 'Failed')
        ],
        db_index=True
    )
    description = models.TextField(
        null=True,
        blank=False
    )

    def __str__(self):
        return f'({self.created}, {self.status} [{self.id}])'

class SystemTimestamp(Standard):
    key = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        db_index=True
    )
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

# --- End: Other models ---