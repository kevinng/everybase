# Generated by Django 3.1.2 on 2021-05-15 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0062_auto_20210513_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user', related_query_name='user', to='relationships.email'),
        ),
    ]
