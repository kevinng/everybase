from django.db import models

"""
Primary key ID is already present in standard models. Parent-Children Choice
fields need to be implemented at model-level.
"""

class Standard():
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, default=None)

class Choice():
    name = models.CharField(max_length=100)
    details_md = models.TextField()

    programmatic_key = models.CharField(max_length=100)
    programmatic_details_md = models.TextField()