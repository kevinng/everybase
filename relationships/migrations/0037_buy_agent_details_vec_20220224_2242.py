from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0036_logistics_agent_details_vec_20220224_2233'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN buy_agent_details_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(buy_agent_details,'')), 'A')
                ) STORED;

                CREATE INDEX buy_agent_details_vec_idx ON relationships_user USING GIN (buy_agent_details_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN buy_agent_details_vec CASCADE;
            '''
        )
    ]