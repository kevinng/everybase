from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0031_last_name_vec_20220224_2202'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN company_name_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(company_name,'')), 'A')
                ) STORED;

                CREATE INDEX company_name_vec_idx ON relationships_user USING GIN (company_name_vec);
            ''',

            # Dropping company_name_vec in 0057
            # reverse_sql = '''
            #     ALTER TABLE relationships_user DROP COLUMN company_name_vec CASCADE;
            # '''
        )
    ]
