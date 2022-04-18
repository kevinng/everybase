from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0037_buy_agent_details_vec_20220224_2242'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN sell_agent_details_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(sell_agent_details,'')), 'A')
                ) STORED;

                CREATE INDEX sell_agent_details_vec_idx ON relationships_user USING GIN (sell_agent_details_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN sell_agent_details_vec CASCADE;
            '''
        )
    ]
