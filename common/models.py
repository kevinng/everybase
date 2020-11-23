from django.db import models
from django.contrib import admin
import uuid

# --- Start: Helper lambda for model field declarations ---

# Foreign key
fk = lambda klass, name=None, verbose_name=None, null=False, db_index=True: \
    models.ForeignKey(
    klass,
    on_delete=models.PROTECT,
    related_name=name,
    related_query_name=name,
    verbose_name=verbose_name,
    null=null,
    blank=null,
    db_index=db_index
)

# Many-to-many
m2m = lambda klass, name, blank=False, db_index=True: models.ManyToManyField(
    klass,
    related_name=name,
    related_query_name=name,
    blank=blank,
    db_index=db_index
)

# Many-to-many through
m2mt = lambda klass, thru, f1, f2, name, db_index=True: models.ManyToManyField(
    klass,
    through=thru,
    through_fields=(f1, f2),
    related_name=name,
    related_query_name=name,
    db_index=db_index
)

# Integer
pintf = lambda verbose_name=None, null=False, db_index=True: models.\
    PositiveIntegerField(verbose_name=verbose_name, null=null, blank=null,
        db_index=db_index)

# Text
tf = lambda verbose_name=None, null=False: models.TextField(
    verbose_name=verbose_name, null=null, blank=null)

# Char
cf = lambda verbose_name=None, null=False, max_length=100, db_index=True: \
    models.CharField(verbose_name=verbose_name, max_length=max_length,
        null=null, blank=null, db_index=db_index)

# Float
ff = lambda verbose_name=None, null=False, db_index=True: models.FloatField(
    verbose_name=verbose_name, null=null, blank=null, db_index=db_index)

# Datetime
dtf = lambda verbose_name=None, null=False, default=None, db_index=True: \
    models.DateTimeField( verbose_name=verbose_name, null=null, blank=null, \
    default=default, db_index=db_index)

dtf_now_add = lambda verbose_name=None, null=False, auto_now_add=True, \
    db_index=True: models.DateTimeField(verbose_name=verbose_name, null=null, \
    blank=null, auto_now_add=auto_now_add, db_index=db_index)

dtf_now = lambda verbose_name=None, null=False, auto_now=True, db_index=True: \
    models.DateTimeField(verbose_name=verbose_name, null=null, blank=null,
    auto_now=auto_now, db_index=db_index)

# URL

url = lambda verbose_name=None, null=False, db_index=True: models.URLField(
    verbose_name=verbose_name, null=null, blank=null, db_index=db_index)

# Email

eml = lambda verbose_name=None, null=False, db_index=True: models.EmailField(
    verbose_name=verbose_name, null=null, blank=null, db_index=db_index)

# UUID

uid = lambda: models.UUIDField(unique=True, default=uuid.uuid4, editable=False,
    db_index=True)

# --- End: Helper lambda for model field declarations ---

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
    created = dtf_now_add()
    updated = dtf_now(null=True)
    deleted = dtf(null=True)

    class Meta:
        abstract = True

choice_fieldnames = ['name', 'details_md', 'programmatic_key',
    'programmatic_details_md']
class Choice(models.Model):
    """
    Abstract model for a choice model.
    """
    name = cf(db_index=True)
    details_md = tf('Details in Markdown', null=True)

    programmatic_key = cf(null=True, db_index=True)
    programmatic_details_md = tf('Programmatic details in Markdown', null=True)

    def __str__(self):
        return '(%s [%d])' % (self.name, self.id)

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
    cc_tld = cf('CC TLD', null=True, db_index=True)
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class State(Choice):
    country = fk('Country', 'states')

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
        db_index=True
    )
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True
    )

# --- End: Other models ---