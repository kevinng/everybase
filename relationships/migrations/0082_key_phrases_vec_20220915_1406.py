from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0081_alert'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_alert ADD COLUMN key_phrases_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(key_phrases,'')), 'A')
                ) STORED;

                CREATE INDEX key_phrases_vec_idx ON relationships_alert USING GIN (key_phrases_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_alert DROP COLUMN key_phrases_vec CASCADE;
            '''
        )
    ]
