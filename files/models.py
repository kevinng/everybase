from django.db import models
from common.models import Standard, ParentChildrenChoice

# --- Start: Helper lambda for model field declarations ---

# Foreign key
fk = lambda klass, name=None, verbose_name=None, null=False: models.ForeignKey(
    klass,
    on_delete=models.PROTECT,
    related_name=name,
    related_query_name=name,
    verbose_name=verbose_name,
    null=null,
    blank=null
)

# Many-to-many
m2m = lambda klass, name, blank=False: models.ManyToManyField(
    klass,
    related_name=name,
    related_query_name=name,
    blank=blank
)

# Many-to-many through
m2mt = lambda klass, thru, f1, f2, name: models.ManyToManyField(
    klass,
    through=thru,
    through_fields=(f1, f2),
    related_name=name,
    related_query_name=name
)

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
    null=null, blank=null, default=default)

# --- End: Helper lambda for model field declarations ---

class FileTag(ParentChildrenChoice):
    pass

class File(Standard):
    source_person = fk('relationships.Person', 'files', null=True)
    source_issue = fk('communication.Issue', 'files', null=True)

    s3_url = models.URLField()
    details_md = tf('Details in Markdown', True)

    anonymization_source = fk('self', 'anonymization_copies', null=True)
    
    tags = fk('FileTag', 'files', null=True)