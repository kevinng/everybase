# Generated by Django 3.1.2 on 2020-11-03 14:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0011_auto_20201103_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
