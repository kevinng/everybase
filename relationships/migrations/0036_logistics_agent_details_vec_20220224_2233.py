from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0035_state_string_vec_20220224_2219'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN logistics_agent_details_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(logistics_agent_details,'')), 'A')
                ) STORED;

                CREATE INDEX logistics_agent_details_vec_idx ON relationships_user USING GIN (logistics_agent_details_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN logistics_agent_details_vec CASCADE;
            '''
        )
    ]
