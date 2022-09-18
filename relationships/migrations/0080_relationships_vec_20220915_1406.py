from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0079_auto_20220915_1406'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_requirement ADD COLUMN requirements_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(requirements,'')), 'A')
                ) STORED;

                CREATE INDEX requirements_vec_idx ON relationships_requirement USING GIN (requirements_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_requirement DROP COLUMN requirements_vec CASCADE;
            '''
        )
    ]
