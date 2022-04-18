from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0029_auto_20220224_2140'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN first_name_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(first_name,'')), 'A')
                ) STORED;

                CREATE INDEX first_name_vec_idx ON relationships_user USING GIN (first_name_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN first_name_vec CASCADE;
            '''
        )
    ]
