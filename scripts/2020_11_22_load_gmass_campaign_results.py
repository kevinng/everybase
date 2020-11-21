import requests
import csv
import os
from growth.tasks import load_gmass_campaign_results

def run():
    id = '63d7d845-a384-4f24-8cdd-aad77f1e360f'
    load_gmass_campaign_results(id)
    

    

    

    # with open('./scripts/out.csv', 'r') as file:
    #     reader = csv.DictReader(file)
    #     print(reader.fieldnames)

    # print(data)