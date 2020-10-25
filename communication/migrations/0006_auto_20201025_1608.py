# Generated by Django 3.1.2 on 2020-10-25 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0005_auto_20201025_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='deleted',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='conversationchat',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='conversationchat',
            name='deleted',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='conversationchat',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='conversationemail',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='conversationemail',
            name='deleted',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='conversationemail',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='conversationvideo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='conversationvideo',
            name='deleted',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='conversationvideo',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='conversationvoice',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='conversationvoice',
            name='deleted',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='conversationvoice',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='deleted',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='scheduled',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True),
        ),
    ]
