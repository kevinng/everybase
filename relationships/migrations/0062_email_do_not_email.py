# Generated by Django 3.1.2 on 2022-05-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0061_user_fb_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='do_not_email',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]