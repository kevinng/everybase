from django.db import models
from common.models import fk, m2m, m2mt, tf, cf, ff, dtf
from common.models import Standard, ParentChildrenChoice

class FileTag(ParentChildrenChoice):
    pass

class File(Standard):
    source_person = fk('relationships.Person', 'files', null=True)
    source_issue = fk('communication.Issue', 'files', null=True)

    s3_url = models.URLField()
    details_md = tf('Details in Markdown', True)

    anonymization_source = fk('self', 'anonymization_copies', null=True)
    
    tags = fk('FileTag', 'files', null=True)