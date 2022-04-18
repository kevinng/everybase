from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0050_commission_type_other_vec_20220224_1622'),
    ]

    operations = [
        # commission_payable_after_other_vec, tsvector
        migrations.RunSQL(
            sql='''
                ALTER TABLE leads_lead ADD COLUMN commission_payable_after_other_vec tsvector GENERATED ALWAYS AS (
                    setweight(to_tsvector('english', coalesce(commission_payable_after_other,'')), 'A')
                ) STORED;

                CREATE INDEX leads_commission_payable_after_other_vec_idx ON leads_lead USING GIN (commission_payable_after_other_vec);
            ''',

            reverse_sql = '''
                ALTER TABLE leads_lead DROP COLUMN commission_payable_after_other_vec CASCADE;
            '''
        )
    ]
