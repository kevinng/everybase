# Generated by Django 3.1.2 on 2020-12-18 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0040_auto_20201219_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='ltype',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='relationships.linktype', verbose_name='Link type'),
        ),
    ]
