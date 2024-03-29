# Generated by Django 3.1.2 on 2022-10-06 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0095_user_walked_through_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='reviewee',
        ),
        migrations.AddField(
            model_name='review',
            name='phone_number',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='reviews', related_query_name='reviews', to='relationships.phonenumber'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='status_updated',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_code_purpose',
            field=models.CharField(blank=True, choices=[('LOGIN', 'LOGIN'), ('VERIFY_EMAIL', 'VERIFY_EMAIL')], db_index=True, max_length=20, null=True),
        ),
    ]
