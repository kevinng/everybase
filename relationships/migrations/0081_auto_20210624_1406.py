# Generated by Django 3.1.2 on 2021-06-24 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0080_auto_20210624_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionanswerpair',
            name='answer_captured',
        ),
        migrations.RemoveField(
            model_name='questionanswerpair',
            name='answer_rewrote',
        ),
        migrations.RemoveField(
            model_name='questionanswerpair',
            name='question_captured',
        ),
        migrations.RemoveField(
            model_name='questionanswerpair',
            name='question_rewrote',
        ),
        migrations.RemoveField(
            model_name='questionanswerpair',
            name='sent_answerer',
        ),
        migrations.AlterField(
            model_name='questionanswerpair',
            name='questioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_answer_pair_questioner', related_query_name='question_answer_pair_questioner', to='relationships.user'),
        ),
    ]