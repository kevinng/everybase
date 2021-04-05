# Generated by Django 3.1.2 on 2021-03-25 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0013_remove_conversation_front_conversation_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversationchat',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='conversationchat',
            name='our_number',
        ),
        migrations.RemoveField(
            model_name='conversationchat',
            name='status',
        ),
        migrations.RemoveField(
            model_name='conversationchat',
            name='their_number',
        ),
        migrations.RemoveField(
            model_name='conversationemail',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='conversationemail',
            name='our_email',
        ),
        migrations.RemoveField(
            model_name='conversationemail',
            name='status',
        ),
        migrations.RemoveField(
            model_name='conversationemail',
            name='their_email',
        ),
        migrations.RemoveField(
            model_name='conversationvideo',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='conversationvideo',
            name='our_number',
        ),
        migrations.RemoveField(
            model_name='conversationvideo',
            name='status',
        ),
        migrations.RemoveField(
            model_name='conversationvideo',
            name='their_number',
        ),
        migrations.RemoveField(
            model_name='conversationvoice',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='conversationvoice',
            name='our_number',
        ),
        migrations.RemoveField(
            model_name='conversationvoice',
            name='status',
        ),
        migrations.RemoveField(
            model_name='conversationvoice',
            name='their_number',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='company',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='demand',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='demand_commission',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='demand_quote',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='match',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='person',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='status',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='supply',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='supply_commission',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='supply_quote',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='issuestatus',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='issuetag',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='ConversationChannel',
        ),
        migrations.DeleteModel(
            name='ConversationChat',
        ),
        migrations.DeleteModel(
            name='ConversationChatStatus',
        ),
        migrations.DeleteModel(
            name='ConversationEmail',
        ),
        migrations.DeleteModel(
            name='ConversationEmailStatus',
        ),
        migrations.DeleteModel(
            name='ConversationVideo',
        ),
        migrations.DeleteModel(
            name='ConversationVideoStatus',
        ),
        migrations.DeleteModel(
            name='ConversationVoice',
        ),
        migrations.DeleteModel(
            name='ConversationVoiceStatus',
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
        migrations.DeleteModel(
            name='IssueStatus',
        ),
        migrations.DeleteModel(
            name='IssueTag',
        ),
    ]