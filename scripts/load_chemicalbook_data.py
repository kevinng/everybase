from leads.models import ChemicalBookSupplier
import datetime
import json_lines

jl_files_root = './raw_data/chemicalbook/'
jl_files = [
    '2020-03-08__alphabets.jl'
]

def run():
    for jl_file in jl_files:
        with open(jl_files_root + jl_file) as opened_file:
            reader = json_lines.reader(opened_file)
            for row in reader:
                supplier = ChemicalBookSupplier()
                supplier.entry_date = datetime.date.today()
                supplier.source_url = row['source_url']
                supplier.coy_name = row['coy_name']
                supplier.coy_internal_href = row['coy_internal_href']
                supplier.coy_tel = row['coy_tel']
                supplier.coy_email = row['coy_email']
                supplier.coy_href = row['coy_href']
                supplier.coy_nat = row['coy_nat']
                supplier.save()

                print('Inserted entry:')
                print(row['source_url'])
                print(row['coy_name'])
                print(row['coy_internal_href'])
                print(row['coy_tel'])
                print(row['coy_email'])
                print(row['coy_href'])
                print(row['coy_nat'])
                print('=====')