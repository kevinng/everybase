# Generated by Django 3.1.2 on 2021-10-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0145_delete_phonenumberlinkaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumberhash',
            name='link_type',
            field=models.CharField(blank=True, choices=[('contact', 'Contact'), ('verification', 'Verification'), ('register', 'Register'), ('login', 'Login')], max_length=20, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='phonenumberhash',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='phonenumberhash',
            name='expired',
        ),
    ]
