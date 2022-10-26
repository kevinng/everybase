# Generated by Django 3.1.2 on 2022-07-13 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0138_auto_20220713_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadflag',
            name='type',
            field=models.CharField(blank=True, choices=[('spam', 'Spam'), ('scam', 'Scam')], db_index=True, max_length=20, null=True),
        ),
    ]