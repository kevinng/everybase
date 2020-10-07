from django.db import models
from common.models import Standard, ParentChildrenChoice

# --- Start: Abstract ---

# Helper function to declare foreign key relationships.
fk = lambda klass, name: models.ForeignKey(
        klass,
        on_delete=models.PROTECT,
        related_name=name,
        related_query_name=name
    )

# --- End: Abstract ---

class FileTag(ParentChildrenChoice):
    pass

class File(Standard):
    source_person = fk('relationships.Person', 'files')
    source_issue = fk('communication.Issue', 'files')

    s3_url = models.CharField(max_length=100)
    details_md = models.TextField()

    anonymization_source = fk('self', 'anonymization_copies')
    
    tags = fk('FileTag', 'files')