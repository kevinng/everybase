from django.db import models
from common.models import Standard, Choice
import uuid

# --- Start: Abstract classes ---

relationship_fieldnames = ['details_md']
class Relationship(Standard):
    details_md = models.TextField(
        'Details in Markdown',
        default=None,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

# --- End: Abstract classes ---

# --- Start: Relationship classes ---

class FileSupplyType(Choice):
    class Meta:
        verbose_name = 'File-supply type'
        verbose_name_plural = 'File-supply types'

class FileSupply(Relationship):
    rtype = models.ForeignKey(
        'FileSupplyType',
        on_delete=models.PROTECT,
        related_name='file_supply_relationships',
        related_query_name='file_supply_relationships',
        verbose_name='File-supply relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    file = models.ForeignKey(
        'File',
        on_delete=models.PROTECT,
        related_name='file_supply_relationships',
        related_query_name='file_supply_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    supply = models.ForeignKey(
        'leads.Supply',
        on_delete=models.PROTECT,
        related_name='file_supply_relationships',
        related_query_name='file_supply_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'FileDemandType',
        on_delete=models.PROTECT,
        related_name='file_demand_relationships',
        related_query_name='file_demand_relationships',
        verbose_name='File-demand relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    file = models.ForeignKey(
        'File',
        on_delete=models.PROTECT,
        related_name='file_demand_relationships',
        related_query_name='file_demand_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    demand = models.ForeignKey(
        'leads.Demand',
        on_delete=models.PROTECT,
        related_name='file_demand_relationships',
        related_query_name='file_demand_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'FileIssueType',
        on_delete=models.PROTECT,
        related_name='file_issue_relationships',
        related_query_name='file_issue_relationships',
        verbose_name='File-issue relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    file = models.ForeignKey(
        'File',
        on_delete=models.PROTECT,
        related_name='file_issue_relationships',
        related_query_name='file_issue_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    issue = models.ForeignKey(
        'communication.Issue',
        on_delete=models.PROTECT,
        related_name='file_issue_relationships',
        related_query_name='file_issue_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'FilePersonType',
        on_delete=models.PROTECT,
        related_name='file_person_relationships',
        related_query_name='file_person_relationships',
        verbose_name='File-person relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    file = models.ForeignKey(
        'File',
        on_delete=models.PROTECT,
        related_name='file_person_relationships',
        related_query_name='file_person_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    person = models.ForeignKey(
        'relationships.Person',
        on_delete=models.PROTECT,
        related_name='file_person_relationships',
        related_query_name='file_person_relationships',
        null=False,
        blank=False,
        db_index=True
    )

    class Meta:
        verbose_name = 'File-person relationship'
        verbose_name_plural = 'File-person relationships'
    
    def __str__(self):
        return f'({self.rtype}, {self.file}, {self.person} [{self.id}])'

# --- End: Relationship classes

# --- Start: File classes ---

class FileTag(Choice):
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        related_query_name='children',
        null=True,
        blank=True,
        db_index=True
    )

class File(Standard):
    upload_confirmed = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    s3_bucket_name = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_key = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_content_length = models.PositiveIntegerField(
        null=True, 
        blank=True,
        db_index=True
    )
    s3_object_e_tag = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_content_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_last_modified = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )

    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=True,
        blank=True
    )

    supplies = models.ManyToManyField(
        'leads.Supply',
        through=FileSupply,
        through_fields=('file', 'supply'),
        related_name='files',
        related_query_name='files',
        db_index=True
    )

    demands = models.ManyToManyField(
        'leads.Demand',
        through=FileDemand,
        through_fields=('file', 'demand'),
        related_name='files',
        related_query_name='files',
        db_index=True
    )

    issues = models.ManyToManyField(
        'communication.Issue',
        through=FileIssue,
        through_fields=('file', 'issue'),
        related_name='files',
        related_query_name='files',
        db_index=True
    )

    persons = models.ManyToManyField(
        'relationships.Person',
        through=FilePerson,
        through_fields=('file', 'person'),
        related_name='files',
        related_query_name='files',
        db_index=True
    )

    tags = models.ManyToManyField(
        'FileTag',
        related_name='files',
        related_query_name='files',
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.s3_bucket_name}, {self.s3_object_key} [{self.id}])'

    class Meta:
        unique_together = ('s3_bucket_name', 's3_object_key')

# --- End: File classes ---