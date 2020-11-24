import requests
from growth.models import GmassCampaign
from growth import tasks

def run():
    # id = '63d7d845-a384-4f24-8cdd-aad77f1e360f'
    # load_gmass_campaign_results.delay(id)
    # load_gmass_campaign_results(id)

    campaign = GmassCampaign.objects.get(pk=3)
    # tasks.load_gmass_campaign_main_report(campaign)

    # tasks.load_gmass_account_bounces(campaign)

    tasks.load_gmass_account_unsubscribes(campaign)



    

    

    

    # with open('./scripts/out.csv', 'r') as file:
    #     reader = csv.DictReader(file)
    #     print(reader.fieldnames)

    # print(data)