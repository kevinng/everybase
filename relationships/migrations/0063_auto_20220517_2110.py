# Generated by Django 3.1.2 on 2022-05-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0062_email_do_not_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='do_not_email',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
    ]