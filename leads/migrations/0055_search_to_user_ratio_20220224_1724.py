from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0054_search_to_lead_ratio_20220224_1646'),
    ]

    operations = [
        # search_to_user_ratio, stored generated column, search_to_user_details_count / search_appearance_count
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN search_to_user_ratio numeric GENERATED ALWAYS AS (
                    search_to_user_details_count / search_appearance_count
                ) STORED;

                CREATE INDEX leads_search_to_user_ratio_idx ON leads_lead(search_to_user_ratio);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN search_to_user_ratio;
                
                DROP INDEX leads_search_to_user_ratio_idx;
            '''
        )
    ]

