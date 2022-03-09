# Generated by Django 3.1.2 on 2022-03-05 13:30

from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    User = apps.get_model('relationships', 'User')
    for row in User.objects.all():
        row.slug_link = uuid.uuid4()
        row.save(update_fields=['slug_link'])

class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0047_auto_20220309_1757'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
