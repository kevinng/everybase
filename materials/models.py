from django.urls import reverse
from django.db import models
import uuid

from accounts.models import Organization

class Material(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

    organization = models.ForeignKey(Organization,
        models.CASCADE, related_name='materials')

    def get_absolute_url(self):
        return reverse('materials:details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + ' (' + self.code + ')'

class Batch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

    material = models.ForeignKey(Material,
        models.CASCADE, related_name='batches')

    class Meta:
        verbose_name_plural = 'Batches'
        unique_together = [['material', 'code']]
    
    def __str__(self):
        return 'ID: %s, Material: %s (%s), Batch: %s' % (str(self.id)[:4], self.material.name, self.material.code, self.code)
    