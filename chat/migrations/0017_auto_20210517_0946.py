# Generated by Django 3.1.2 on 2021-05-17 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0064_auto_20210516_0155'),
        ('chat', '0016_auto_20210516_0155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagetemplate',
            name='chat_context_type',
        ),
        migrations.AddField(
            model_name='userchatcontext',
            name='context',
            field=models.CharField(choices=[('ur', 'User Registration')], db_index=True, default='ur', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='userchatcontext',
            unique_together={('user', 'context')},
        ),
        migrations.RemoveField(
            model_name='userchatcontext',
            name='chat_context_type',
        ),
        migrations.DeleteModel(
            name='ChatContextType',
        ),
    ]