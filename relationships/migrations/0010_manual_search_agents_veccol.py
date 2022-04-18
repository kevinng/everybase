from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0009_user_goods_string'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN search_agents_veccol tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(first_name, '')), 'B') ||
                    setweight(to_tsvector('english', coalesce(last_name,'')), 'B') ||
                    setweight(to_tsvector('english', coalesce(goods_string,'')), 'A') ||
                    setweight(to_tsvector('english', coalesce(languages_string,'')), 'C')
                ) STORED;

                CREATE INDEX relationships_user_search_agents_veccol ON relationships_user USING GIN (search_agents_veccol);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN search_agents_veccol;

                DROP INDEX relationships_user_search_agents_veccol;
            '''
        ),
    ]
