# Generated by Django 3.1.2 on 2022-09-15 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0077_userdetailview_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetailview',
            name='comments_view_count',
        ),
        migrations.RemoveField(
            model_name='userdetailview',
            name='leads_view_count',
        ),
    ]
