# Generated by Django 3.1.2 on 2021-08-11 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0102_remove_email_name'),
        ('growth', '0006_note_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='growth_notes', related_query_name='growth_notes', to='relationships.user'),
        ),
    ]