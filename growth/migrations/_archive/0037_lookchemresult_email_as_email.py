# Generated by Django 3.1.2 on 2020-10-25 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0036_auto_20201025_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookchemresult',
            name='email_as_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]