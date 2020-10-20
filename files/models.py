from django.db import models
from common.models import fk, tf
from common.models import Standard, Choice, short_text

class FileTag(Choice):
    parent = fk('self', 'children', null=True)

class File(Standard):
    source_person = fk('relationships.Person', 'files', null=True)
    source_issue = fk('communication.Issue', 'files', null=True)

    s3_url = models.URLField()
    details_md = tf('Details in Markdown', True)

    anonymization_source = fk('self', 'anonymization_copies', null=True)
    
    tags = fk('FileTag', 'files', null=True)

    def __str__(self):
        return f'({short_text(self.s3_url, backward=True)} [{self.id}])'