from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('leads', '0011_agentquery_ineedagentquery_whatsappclick_whatsappmessagebody'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN search_i_need_agents_veccol tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(details, '')), 'A') ||
                    setweight(to_tsvector('english', coalesce(other_commission_details,'')), 'B')
                ) STORED;

                CREATE INDEX leads_lead_search_i_need_agents_veccol ON leads_lead USING GIN (search_i_need_agents_veccol);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN search_i_need_agents_veccol;

                DROP INDEX leads_lead_search_i_need_agents_veccol;
            '''
        ),
    ]
