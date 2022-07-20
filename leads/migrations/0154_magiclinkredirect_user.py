# Generated by Django 3.1.2 on 2022-07-20 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0072_auto_20220719_1455'),
        ('leads', '0153_magiclinkredirect'),
    ]

    operations = [
        migrations.AddField(
            model_name='magiclinkredirect',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='magic_link_redirects', related_query_name='magic_link_redirects', to='relationships.user'),
        ),
    ]
