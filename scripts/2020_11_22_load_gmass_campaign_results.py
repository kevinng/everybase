import requests
from growth.models import GmassCampaign
from growth.tasks import load_gmass_campaign_main_report

def run():
    # id = '63d7d845-a384-4f24-8cdd-aad77f1e360f'
    # load_gmass_campaign_results.delay(id)
    # load_gmass_campaign_results(id)

    campaign = GmassCampaign.objects.get(pk=3)
    load_gmass_campaign_main_report(campaign)
    


    

    

    

    # with open('./scripts/out.csv', 'r') as file:
    #     reader = csv.DictReader(file)
    #     print(reader.fieldnames)

    # print(data)