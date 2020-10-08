from django.db import models
from django.contrib import admin

# --- Start: Abstract ---

# Helper function to declare foreign key relationships.
fk = lambda klass, name: models.ForeignKey(
    klass,
    on_delete=models.PROTECT,
    related_name=name,
    related_query_name=name
)

class Standard(models.Model):
    """
    Abstract model with standard fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

class Choice(models.Model):
    """
    Abstract model for a choice model.
    """
    name = models.CharField(max_length=100)
    details_md = models.TextField('Details in Markdown',
        null=True,
        blank=True)

    programmatic_key = models.CharField(max_length=100,
        null=True,
        blank=True)
    programmatic_details_md = models.TextField(
        'Programmatic details in Markdown',
        null=True,
        blank=True)

    def __str__(self):
        return '%d, %s' % (self.id, self.name)

    class Meta:
        abstract = True

class ParentChildrenChoice(Choice):
    parent = fk('self', 'children')

# --- End: Abstract ---

class Country(Choice):
    pass

class State(Choice):
    pass