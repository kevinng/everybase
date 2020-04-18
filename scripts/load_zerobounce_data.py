from leads.models import ZeroBounceResult
import csv, datetime, traceback

file_root = './raw_data/zerobounce/'
csv_files = [
    '2020_03_09__all_emails_all_results.csv',
    '2020-03-04_emails_to_test_with_100_free_credits_all_results.csv',
    '2020-03-04_fibre2fabric_leads_minus_100_verified_with_free_credit_all_results.csv',
    '2020-03-04_fibre2fabric_leads_minus_100_verified_with_free_credits_all_results.csv'
]

def run():
    for csv_file in csv_files:
        with open(file_root + csv_file) as opened_file:
            reader = csv.DictReader(opened_file)
            for row in reader:
                try:
                    result = ZeroBounceResult()
                    result.entry_date = datetime.date.today()
                    result.email_address = row['Email Address']
                    result.zb_status = row['ZB Status']
                    result.zb_account = row['ZB Account']
                    result.zb_domain = row['ZB Domain']
                    result.zb_first_name = row['ZB First Name']
                    result.zb_last_name = row['ZB Last Name']
                    result.zb_gender = row['ZB Gender']
                    result.zb_free_email = row['ZB Free Email']
                    result.zb_mx_found = row['ZB MX Found']
                    result.zb_mx_record = row['ZB MX Record']
                    result.zb_smtp_provider = row['ZB SMTP Provider']
                    result.zb_did_you_mean = row['ZB Did You Mean']
                    result.save()
                except:
                    traceback.print_exc()

                print('Inserted entry:')
                print(row['Email Address'])
                print(row['ZB Status'])
                print(row['ZB Sub Status'])
                print(row['ZB Account'])
                print(row['ZB Domain'])
                print(row['ZB First Name'])
                print(row['ZB Last Name'])
                print(row['ZB Gender'])
                print(row['ZB Free Email'])
                print(row['ZB MX Found'])
                print(row['ZB MX Record'])
                print(row['ZB SMTP Provider'])
                print(row['ZB Did You Mean'])
                print('=====')