# Generated by Django 3.1.2 on 2021-09-15 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0116_auto_20210915_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='recommend_immediate_confirm_choice',
            field=models.CharField(blank=True, choices=[('RECOMMEND__IMMEDIATE_CONFIRM', 'RECOMMEND__IMMEDIATE_CONFIRM'), ('RECOMMEND__IMMEDIATE_CONFIRM__YES', 'RECOMMEND__IMMEDIATE_CONFIRM__YES'), ('RECOMMEND__IMMEDIATE_CONFIRM__CANCEL', 'RECOMMEND__IMMEDIATE_CONFIRM__CANCEL')], max_length=200, null=True),
        ),
    ]