from django.db import models
from django.contrib import admin

# --- Start: Helper lambda for model field declarations ---

# Foreign key
fk = lambda klass, name=None, verbose_name=None, null=False, index=True: models.ForeignKey(
    klass,
    on_delete=models.PROTECT,
    related_name=name,
    related_query_name=name,
    verbose_name=verbose_name,
    null=null,
    blank=null,
    db_index=index
)

# Many-to-many
m2m = lambda klass, name, blank=False, index=True: models.ManyToManyField(
    klass,
    related_name=name,
    related_query_name=name,
    blank=blank,
    db_index=index
)

# Many-to-many through
m2mt = lambda klass, thru, f1, f2, name: models.ManyToManyField(
    klass,
    through=thru,
    through_fields=(f1, f2),
    related_name=name,
    related_query_name=name
)

# Integer
pintf = lambda verbose_name=None, null=False: models.PositiveIntegerField(
    verbose_name=verbose_name, null=null, blank=null)

# Text
tf = lambda verbose_name=None, null=False: models.TextField(
    verbose_name=verbose_name, null=null, blank=null)

# Char
cf = lambda verbose_name=None, null=False: models.CharField(
    verbose_name=verbose_name, max_length=100, null=null, blank=null)

# Float
ff = lambda verbose_name=None, null=False: models.FloatField(
    verbose_name=verbose_name, null=null, blank=null)

# Datetime
dtf = lambda verbose_name=None, null=False, default=None: models.DateTimeField(
    verbose_name=verbose_name, null=null, blank=null, default=default)

dtf_now_add = lambda verbose_name=None, null=False, auto_now_add=True: models.\
    DateTimeField(verbose_name=verbose_name, null=null, blank=null,
    auto_now_add=auto_now_add)

dtf_now = lambda verbose_name=None, null=False, auto_now=True: models.\
    DateTimeField(verbose_name=verbose_name, null=null, blank=null,
    auto_now=auto_now)

# URL

url = lambda verbose_name=None, null=False: models.URLField(
    verbose_name=verbose_name, null=null, blank=null)

# Email

eml = lambda verbose_name=None, null=False: models.EmailField(
    verbose_name=verbose_name, null=null, blank=null)

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

class Standard(models.Model):
    """
    Abstract model with standard fields.
    """
    created = dtf_now_add()
    updated = dtf_now(null=True)
    deleted = dtf(null=True)

    class Meta:
        abstract = True

standard_fieldnames = ['created', 'updated', 'deleted']

class Choice(models.Model):
    """
    Abstract model for a choice model.
    """
    name = cf()
    details_md = tf('Details in Markdown', null=True)

    programmatic_key = cf(null=True)
    programmatic_details_md = tf('Programmatic details in Markdown', null=True)

    def __str__(self):
        return '(%s [%d])' % (self.name, self.id)

    class Meta:
        abstract = True

choice_fieldnames = ['name', 'details_md', 'programmatic_key',
    'programmatic_details_md']

# --- End: Abstract models ---

# --- Start: Common models ---

class Country(Choice):
    cc_tld = cf('CC TLD', null=True)
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class State(Choice):
    country = fk('Country', 'states')

# --- End: Common models ---