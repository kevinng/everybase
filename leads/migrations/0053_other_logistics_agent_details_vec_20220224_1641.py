from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0052_other_agent_details_vec_20220224_1636'),
    ]

    operations = [
        # other_logistics_agent_details_vec, tsvector
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN other_logistics_agent_details_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(other_logistics_agent_details,'')), 'A')
                ) STORED;

                CREATE INDEX leads_other_logistics_agent_details_vec_idx ON leads_lead USING GIN (other_logistics_agent_details_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN other_logistics_agent_details_vec;
                
                DROP INDEX public.leads_other_logistics_agent_details_vec_idx
            '''
        )
    ]
