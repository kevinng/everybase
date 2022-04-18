from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0088_auto_20220413_1812'),
    ]

    operations = [
        # details_vec, tsvector
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN headline_details_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(headline,'')), 'A') ||
                    setweight(to_tsvector('english', coalesce(details,'')), 'B')
                ) STORED;

                CREATE INDEX headline_details_vec_idx ON leads_lead USING GIN (details_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN headline_details_vec CASCADE;
            '''
        )
    ]
