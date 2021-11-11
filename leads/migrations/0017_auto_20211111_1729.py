# Generated by Django 3.1.2 on 2021-11-11 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0016_lead_commission_payable_by'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='leaddocumentaccess',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='leaddocumentaccess',
            name='accessor',
        ),
        migrations.RemoveField(
            model_name='leaddocumentaccess',
            name='lead_document',
        ),
        migrations.RemoveField(
            model_name='leadimage',
            name='file',
        ),
        migrations.RemoveField(
            model_name='leadimage',
            name='lead',
        ),
        migrations.AlterUniqueTogether(
            name='leadimageaccess',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='leadimageaccess',
            name='accessor',
        ),
        migrations.RemoveField(
            model_name='leadimageaccess',
            name='lead_image',
        ),
        migrations.DeleteModel(
            name='LeadDocument',
        ),
        migrations.DeleteModel(
            name='LeadDocumentAccess',
        ),
        migrations.DeleteModel(
            name='LeadImage',
        ),
        migrations.DeleteModel(
            name='LeadImageAccess',
        ),
    ]
