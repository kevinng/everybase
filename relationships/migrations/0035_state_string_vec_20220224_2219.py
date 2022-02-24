from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0034_languages_string_vec_20220224_2218'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN state_string_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(state_string,'')), 'A')
                ) STORED;

                CREATE INDEX state_string_vec_idx ON relationships_user USING GIN (state_string_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN state_string_vec CASCADE;
            '''
        )
    ]
