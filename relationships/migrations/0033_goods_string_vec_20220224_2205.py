from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0032_company_name_vec_20220224_2204'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN goods_string_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(goods_string,'')), 'A')
                ) STORED;

                CREATE INDEX goods_string_vec_idx ON relationships_user USING GIN (goods_string_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN goods_string_vec CASCADE;
            '''
        )
    ]
