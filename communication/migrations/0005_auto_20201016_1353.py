# Generated by Django 3.0.5 on 2020-10-16 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0001_initial'),
        ('communication', '0004_auto_20201016_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversationemail',
            name='our_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='conversation_email_ours', related_query_name='conversation_email_ours', to='relationships.Email'),
        ),
        migrations.AlterField(
            model_name='conversationemail',
            name='their_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='conversation_email_theirs', related_query_name='conversation_email_theirs', to='relationships.Email'),
        ),
    ]
