from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0048_auto_20220224_1509'),
    ]

    operations = [
        # details_vec, tsvector
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN details_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(details,'')), 'A')
                ) STORED;

                CREATE INDEX leads_details_vec_idx ON leads_lead USING GIN (details_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN details_vec CASCADE;
            '''
        )
    ]
