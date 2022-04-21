# Generated by Django 3.1.2 on 2022-03-15 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0052_remove_user_saved_count'),
        ('payments', '0002_auto_20220303_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripecustomer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='relationships.user'),
        ),
        migrations.AlterUniqueTogether(
            name='stripecustomer',
            unique_together=set(),
        ),
    ]