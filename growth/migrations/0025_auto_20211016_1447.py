# Generated by Django 3.1.2 on 2021-10-16 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0024_auto_20210830_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noteupdate',
            name='notes',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='NoteAgenda',
        ),
        migrations.DeleteModel(
            name='NoteOutcome',
        ),
        migrations.DeleteModel(
            name='NoteUpdate',
        ),
    ]