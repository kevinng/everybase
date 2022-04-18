from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0041_auto_20220228_0048'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN company_name_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(company_name,'')), 'A')
                ) STORED;

                CREATE INDEX company_name_vec_idx ON relationships_user USING GIN (company_name_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN company_name_vec CASCADE;
            '''
        )
    ]
