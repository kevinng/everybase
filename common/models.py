from django.db import models

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
    details_md = models.TextField()

    programmatic_key = models.CharField(max_length=100)
    programmatic_details_md = models.TextField()

    class Meta:
        abstract = True

class ParentChildrenChoice(Choice):
    parent = fk('self', 'children')

# --- End: Abstract ---

class Country(Choice):
    pass

class State(Choice):
    pass