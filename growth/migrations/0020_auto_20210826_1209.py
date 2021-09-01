# Generated by Django 3.1.2 on 2021-08-26 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('growth', '0019_remove_note_cc_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notestatus',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='notetag',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='note',
            name='contact_group',
        ),
        migrations.RemoveField(
            model_name='note',
            name='text',
        ),
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
        migrations.DeleteModel(
            name='ContactGroup',
        ),
        migrations.DeleteModel(
            name='NoteStatus',
        ),
        migrations.DeleteModel(
            name='NoteTag',
        ),
    ]