# Generated by Django 3.1.2 on 2021-05-04 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0009_auto_20210428_1522'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestMessageGroup',
            new_name='TestMessage',
        ),
        migrations.RemoveField(
            model_name='groupingmethod',
            name='inbound_message_group',
        ),
        migrations.RemoveField(
            model_name='groupingmethod',
            name='method',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegroup',
            name='twilio_inbound_messages',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegrouprelationship',
            name='demand_quotes',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegrouprelationship',
            name='demands',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegrouprelationship',
            name='group',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegrouprelationship',
            name='supplies',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegrouprelationship',
            name='supply_quotes',
        ),
        migrations.RemoveField(
            model_name='inboundmessagegrouprelationship',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='method',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='operationmethod',
            name='inbound_message_group',
        ),
        migrations.RemoveField(
            model_name='operationmethod',
            name='method',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='test_run_type',
        ),
        migrations.RemoveField(
            model_name='testrunresult',
            name='method',
        ),
        migrations.RemoveField(
            model_name='testrunresult',
            name='test_message_group',
        ),
        migrations.RemoveField(
            model_name='testrunresult',
            name='test_run',
        ),
        migrations.RemoveField(
            model_name='testruntype',
            name='methods',
        ),
        migrations.DeleteModel(
            name='BaseTruth',
        ),
        migrations.DeleteModel(
            name='GroupingMethod',
        ),
        migrations.DeleteModel(
            name='InboundMessageGroup',
        ),
        migrations.DeleteModel(
            name='InboundMessageGroupRelationship',
        ),
        migrations.DeleteModel(
            name='InboundMessageGroupRelationshipTag',
        ),
        migrations.DeleteModel(
            name='Method',
        ),
        migrations.DeleteModel(
            name='MethodTag',
        ),
        migrations.DeleteModel(
            name='OperationMethod',
        ),
        migrations.DeleteModel(
            name='TestRun',
        ),
        migrations.DeleteModel(
            name='TestRunResult',
        ),
        migrations.DeleteModel(
            name='TestRunType',
        ),
    ]
