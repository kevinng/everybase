# Generated by Django 3.1.2 on 2021-06-24 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0098_auto_20210623_2246'),
        ('relationships', '0081_auto_20210624_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionanswerpair',
            name='answer_auto_cleaned',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='answer_captured_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qnas_w_this_answer_captured_value', related_query_name='qnas_w_this_answer_captured_value', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='answer_forwarded',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='answer_forwarded_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qnas_w_this_answer_forwarded_message', related_query_name='qnas_w_this_answer_forwarded_message', to='chat.twiliooutboundmessage'),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='answer_ready',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='auto_cleaned_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='auto_cleaned_answer_w_mark_up',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='auto_cleaned_question',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='auto_cleaned_question_w_mark_up',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='manual_cleaned_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='manual_cleaned_question',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='question_auto_cleaned',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='question_captured_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qnas_w_this_question_captured_value', related_query_name='qnas_w_this_question_captured_value', to='chat.messagedatavalue'),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='question_forwarded',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='question_forwarded_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='qnas_w_this_question_forwarded_message', related_query_name='qnas_w_this_question_forwarded_message', to='chat.twiliooutboundmessage'),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='question_ready',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='use_auto_cleaned_answer',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='use_auto_cleaned_question',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionanswerpair',
            name='answerer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='qnas_w_this_answerer', related_query_name='qnas_w_this_answerer', to='relationships.user'),
        ),
        migrations.AlterField(
            model_name='questionanswerpair',
            name='questioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='qnas_w_this_questioner', related_query_name='qnas_w_this_questioner', to='relationships.user'),
        ),
    ]