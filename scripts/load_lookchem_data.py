from leads.models import LookChemSupplier
import datetime
import json_lines

jl_files_root = './raw_data/lookchem/'
jl_files = [
    '2020-03-09__suppliers.jl'
]

def run():
    for jl_file in jl_files:
        with open(jl_files_root + jl_file) as opened_file:
            reader = json_lines.reader(opened_file)
            for row in reader:
                supplier = LookChemSupplier()
                supplier.entry_date = datetime.date.today()
                supplier.coy_name = row['coy_name']
                supplier.contact_person = row['contact_person']
                supplier.street_person = row['street_address']
                supplier.city = row['city']
                supplier.province_state = row['province_state']
                supplier.country_region = row['country_region']
                supplier.zip_code = row['zip_code']
                supplier.business_type = row['business_type']
                supplier.tel = row['tel']
                supplier.mobile = row['mobile']
                supplier.email = row['email']
                supplier.website = row['website']
                supplier.qq = row['qq']
                supplier.save()

                print('Inserted entry:')
                print(row['coy_name'])
                print(row['contact_person'])
                print(row['street_address'])
                print(row['city'])
                print(row['province_state'])
                print(row['country_region'])
                print(row['zip_code'])
                print(row['business_type'])
                print(row['tel'])
                print(row['mobile'])
                print(row['email'])
                print(row['website'])
                print(row['qq'])
                print('=====')