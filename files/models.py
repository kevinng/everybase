from django.db import models
from common.models import fk, uid, dtf, cf, pintf, tf, m2mt, m2m
from common.models import Standard, Choice

# --- Start: Abstract classes ---

relationship_fieldnames = ['details_md']
class Relationship(Standard):
    details_md = tf('Details in Markdown')

    class Meta:
        abstract = True

# --- End: Abstract classes ---

# --- Start: Relationship classes ---

class FileSupplyType(Choice):
    class Meta:
        verbose_name = 'File-supply type'
        verbose_name_plural = 'File-supply types'

class FileSupply(Relationship):
    rtype = fk('FileSupplyType', 'file_supply_relationships',
        'File-supply relationship type')
    file = fk('File', 'file_supply_relationships')
    supply = fk('leads.Supply', 'file_supply_relationships')

    class Meta:
        verbose_name = 'File-supply relationship'
        verbose_name_plural = 'File-supply relationships'
    
    def __str__(self):
        return f'({self.rtype}, {self.afile}, {self.supply} [{self.id}])'

class FileDemandType(Choice):
    class Meta:
        verbose_name = 'File-demand type'
        verbose_name_plural = 'File-demand types'

class FileDemand(Relationship):
    rtype = fk('FileDemandType', 'file_demand_relationships',
        'File-demand relationship type')
    file = fk('File', 'file_demand_relationships')
    demand = fk('leads.Demand', 'file_demand_relationships')

    class Meta:
        verbose_name = 'File-demand relationship'
        verbose_name_plural = 'File-demand relationships'
    
    def __str__(self):
        return f'({self.rtype}, {self.file}, {self.demand} [{self.id}])'

class FileIssueType(Choice):
    class Meta:
        verbose_name = 'File-issue type'
        verbose_name_plural = 'File-issue types'

class FileIssue(Relationship):
    rtype = fk('FileIssueType', 'file_issue_relationships',
        'File-issue relationship type')
    file = fk('File', 'file_issue_relationships')
    issue = fk('communication.Issue', 'file_issue_relationships')

    class Meta:
        verbose_name = 'File-issue relationship'
        verbose_name_plural = 'File-issue relationships'
    
    def __str__(self):
        return f'({self.rtype}, {self.file}, {self.issue} [{self.id}])'

class FilePersonType(Choice):
    class Meta:
        verbose_name = 'File-person type'
        verbose_name_plural = 'File-person types'

class FilePerson(Relationship):
    rtype = fk('FilePersonType', 'file_person_relationships',
        'File-person relationship type')
    file = fk('File', 'file_person_relationships')
    person = fk('relationships.Person', 'file_person_relationships')

    class Meta:
        verbose_name = 'File-person relationship'
        verbose_name_plural = 'File-person relationships'
    
    def __str__(self):
        return f'({self.rtype}, {self.file}, {self.person} [{self.id}])'

# --- End: Relationship classes

# --- Start: File classes ---

class FileTag(Choice):
    parent = fk('self', 'children', null=True)

class File(Standard):
    uuid = uid()
    upload_confirmed = dtf()

    s3_bucket_name = cf(max_length=63, null=True)
    s3_object_key = cf(max_length=1024, null=True)
    s3_object_content_length = pintf(null=True)
    s3_object_e_tag = cf(null=True)
    s3_object_content_type = cf(null=True)
    s3_object_last_modified = dtf(null=True)

    details_md = tf('Details in Markdown', True)

    supplies = m2mt(
        'leads.Supply',
        'FileSupply',
        'file', 'supply',
        'files'
    )

    demands = m2mt(
        'leads.Demand',
        'FileDemand',
        'file', 'demand',
        'files'
    )

    issues = m2mt(
        'communication.Issue',
        'FileIssue',
        'file', 'issue',
        'files'
    )

    persons = m2mt(
        'relationships.Person',
        'FilePerson',
        'file', 'person',
        'files'
    )

    tags = m2m('FileTag', 'files', blank=True)

    def __str__(self):
        return f'({self.uuid} [{self.id}])'

    class Meta:
        unique_together = ('s3_bucket_name', 's3_object_key')

# --- End: File classes ---