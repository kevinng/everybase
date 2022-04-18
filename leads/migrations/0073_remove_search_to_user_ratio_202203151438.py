from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0072_delete_agentquery'),
    ]

    operations = [
        # search_to_user_ratio, stored generated column, search_to_user_details_count / search_appearance_count
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead DROP COLUMN search_to_user_ratio CASCADE;
            '''
        )
    ]

