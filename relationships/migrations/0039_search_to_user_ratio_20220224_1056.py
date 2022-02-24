from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0038_sell_agent_details_vec_20220224_2247'),
    ]

    operations = [
        # search_to_user_ratio, stored generated column, search_to_user_count / search_appearance_count
        migrations.RunSQL(
            sql='''
                ALTER TABLE relationships_user ADD COLUMN search_to_user_ratio numeric GENERATED ALWAYS AS (
                    search_to_user_count / search_appearance_count
                ) STORED;

                CREATE INDEX relationships_search_to_user_ratio_idx ON relationships_user(search_to_user_ratio);
            ''',

            reverse_sql = '''
                ALTER TABLE relationships_user DROP COLUMN search_to_user_ratio CASCADE;
            '''
        )
    ]

