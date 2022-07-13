from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0136_auto_20220713_0404'),
    ]

    operations = [
        # body_vec, tsvector
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN body_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(body,'')), 'A')
                ) STORED;

                CREATE INDEX body_vec_idx ON leads_lead USING GIN (body_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN body_vec CASCADE;
            '''
        )
    ]
