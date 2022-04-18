from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0033_goods_string_vec_20220224_2205'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN languages_string_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(languages_string,'')), 'A')
                ) STORED;

                CREATE INDEX languages_string_vec_idx ON relationships_user USING GIN (languages_string_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN languages_string_vec CASCADE;
            '''
        )
    ]
