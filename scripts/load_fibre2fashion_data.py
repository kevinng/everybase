from leads.models import Fibre2FashionLead
import datetime
import json_lines

jl_files_root = './raw_data/fibre2fashion/'
jl_files = [
    '2020-02-28_dye_and_yarn__buyers.jl',
    '2020-02-28_dye_and_yarn__suppliers.jl',
    '2020-02-29_fibre_and_fabric__suppliers.jl',
    '2020-02-29_other__buyers.jl',
    '2020-02-29_other__suppliers.jl',
    '2020-03-03_fibre_and_fabric__buyers.jl',
]

def run():
    for jl_file in jl_files:
        with open(jl_files_root + jl_file) as opened_file:
            reader = json_lines.reader(opened_file)
            for row in reader:
                lead = Fibre2FashionLead()
                lead.entry_date = datetime.date.today()
                lead.url = row.get('url', '')
                lead.cat = row.get('cat', '')
                lead.subcat = row.get('subcat', '')
                lead.title = row.get('title', '')
                lead.ref_no = row.get('ref_no', '')
                lead.biz_lead = row.get('biz_lead', '')
                lead.coy_des = row.get('coy_des', '')
                lead.coy_email = row.get('coy_email', '')
                lead.prod_info_html = row.get('prod_info_html', '')
                lead.coy_name = row.get('coy_name', '')
                lead.coy_addr = row.get('coy_addr', '')
                lead.save()

                print('Inserted entry:')
                print(row.get('url', ''))
                print(row.get('cat', ''))
                print(row.get('subcat', ''))
                print(row.get('title', ''))
                print(row.get('ref_no', ''))
                print(row.get('biz_lead', ''))
                print(row.get('coy_des', ''))
                print(row.get('coy_email', ''))
                print(row.get('prod_info_html', '')[:100])
                print(row.get('coy_name', ''))
                print(row.get('coy_addr', ''))
                print('=====')