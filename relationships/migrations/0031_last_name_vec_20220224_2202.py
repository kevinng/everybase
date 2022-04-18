from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0030_first_name_vec_20220224_2145'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN last_name_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(last_name,'')), 'A')
                ) STORED;

                CREATE INDEX last_name_vec_idx ON relationships_user USING GIN (last_name_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN last_name_vec CASCADE;
            '''
        )
    ]
