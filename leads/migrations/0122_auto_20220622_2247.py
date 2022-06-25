# Generated by Django 3.1.2 on 2022-06-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0121_auto_20220622_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='purpose',
        ),
        migrations.AddField(
            model_name='contact',
            name='is_buy_comm',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_buyer',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_sell_comm',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_seller',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
