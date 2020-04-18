from leads.models import WorldOfChemicalsSupplier
import datetime
import json_lines

jl_files_root = './raw_data/worldofchemicals/'
jl_files = [
    '2020-03-08__suppliers.jl'
]

def run():
    # Read World-of-Chemicals data and insert into database
    for jl_file in jl_files:
        with open(jl_files_root + jl_file) as opened_file:
            reader = json_lines.reader(opened_file)
            for row in reader:
                supplier = WorldOfChemicalsSupplier()
                supplier.entry_date = datetime.date.today()
                supplier.coy_id = row['coy_id']
                supplier.coy_name = row['coy_name']
                supplier.coy_about_html = row['coy_about_html']
                supplier.coy_addr_1 = row['coy_addr_1']
                supplier.coy_addr_2 = row['coy_addr_2']
                supplier.coy_city = row['coy_city']
                supplier.coy_state = row['coy_state']
                supplier.coy_country = row['coy_country']
                supplier.coy_postal = row['coy_postal']
                supplier.coy_phone = row['coy_phone']
                supplier.coy_phone_2 = row['coy_phone_2']
                supplier.coy_email = row['coy_email']
                supplier.coy_owner_email = row['coy_owner_email']
                supplier.coy_alt_email = row['coy_alt_email']
                supplier.coy_alt_email_2 = row['coy_alt_email_2']
                supplier.coy_alt_email_3 = row['coy_alt_email_3']
                supplier.coy_website = row['coy_website']
                supplier.save()

                print('Inserted entry:')
                print(row['coy_id'])
                print(row['coy_name'])
                print(row['coy_about_html'][:100])
                print(row['coy_pri_contact'])
                print(row['coy_addr_1'])
                print(row['coy_addr_2'])
                print(row['coy_city'])
                print(row['coy_state'])
                print(row['coy_country'])
                print(row['coy_postal'])
                print(row['coy_phone'])
                print(row['coy_phone_2'])
                print(row['coy_email'])
                print(row['coy_owner_email'])
                print(row['coy_alt_email'])
                print(row['coy_alt_email_2'])
                print(row['coy_alt_email_3'])
                print(row['coy_website'])
                print('=====')