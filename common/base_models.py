from django.db import models

class Standard(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, default=None)

class Choice(models.Model):
    name = models.CharField(max_length=100)
    details_md = models.TextField()

    programmatic_key = models.CharField(max_length=100)
    programmatic_details_md = models.TextField()

class ParentChildrenChoice(Choice):
    parent = 'self', on_delete=models.PROTECT, related_name='children')