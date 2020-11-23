import traceback
import requests
import os
import csv
import io
import datetime
import pytz

from growth.models import GmassCampaignResult
from celery import shared_task
from scripts.shared import helpers
from relationships.shared import record_email
from django.core.exceptions import ValidationError
from everybase.settings import TIME_ZONE

def get_gmass_campaign_id(gmass_campaign):
    return gmass_campaign.report_url\
        .split('?')[-1]\
        .split('&')[0]\
        .split('=')[1]

@shared_task
def load_gmass_account_unsubscribes(gmass_campaign):
    """
    Note: we provide the campaign ID though we're requesting for account-level
    unsubscribes.
    """

    id = get_gmass_campaign_id(gmass_campaign)

    # Download CSV file as data (without materializing into file)
    download_url = \
        f'https://www.gmass.co/gmass/DownloadCSV?C={id}&RT=ua'
    data = requests.get(download_url).json()['data']

    # Parse CSV file in-memory with StringIO
    reader = csv.DictReader(io.StringIO(data))

    print(reader.fieldnames)

    # TODO: to be implemented

@shared_task
def load_gmass_account_bounces(gmass_campaign):
    """
    Note: we provide the campaign ID though we're requesting for account-level
    bounces.
    """

    id = get_gmass_campaign_id(gmass_campaign)

    # Download CSV file as data (without materializing into file)
    download_url = \
        f'https://www.gmass.co/gmass/DownloadCSV?C={id}&RT=ba'
    data = requests.get(download_url).json()['data']

    # Parse CSV file in-memory with StringIO
    reader = csv.DictReader(io.StringIO(data))

    print(reader.fieldnames)

    # TODO: to be implemented

@shared_task
def load_gmass_campaign_main_report(gmass_campaign):

    id = get_gmass_campaign_id(gmass_campaign)

    # Download CSV file as data (without materializing into file)
    download_url = \
        f'https://www.gmass.co/gmass/downloadcsvaction?C={id}&RT=m'
    data = requests.get(download_url).json()['data']

    # Parse CSV file in-memory with StringIO
    reader = csv.DictReader(io.StringIO(data))

    row_created_count = 0
    row_updated_count = 0
    for row in reader:
        email_address = helpers.clean_string(row.get('emailaddress', None))

        (email, invalid_email) = record_email(email_address)

        first_name = helpers.clean_string(row.get('firstname', None))
        last_name = helpers.clean_string(row.get('lastname', None))
        name_1 = helpers.clean_string(row.get('name1', None))
        opens = helpers.clean_integer(row.get('Opens', None))
        clicks = helpers.clean_integer(row.get('Clicks', None))
        replied = helpers.clean_string(row.get('Replied', None))
        unsubscribed = helpers.clean_string(row.get('Unsubscribed', None))
        bounced = helpers.clean_string(row.get('Bounced', None))
        blocked = helpers.clean_string(row.get('Blocked', None))
        over_gmail_limit = helpers.clean_string(row.get('OverGmailLimit', None))
        gmail_response = helpers.clean_string(row.get('GmailResponse', None))

        # Get result for this campaign with its email (an email is unique for
        # a campaign)
        try:
            result = GmassCampaignResult.objects.get(
                email_address=email_address,
                gmass_campaign=gmass_campaign
            )
            row_updated_count += 1
        except GmassCampaignResult.DoesNotExist:
            result = GmassCampaignResult(
                email_address=email_address,
                gmass_campaign=gmass_campaign
            )
            row_created_count += 1

        result.first_name = first_name
        result.last_name = last_name
        result.name_1 = name_1
        result.opens = opens
        result.clicks = clicks
        result.replied = replied
        result.unsubscribed = unsubscribed
        result.bounced = bounced
        result.blocked = blocked
        result.over_gmail_limit = over_gmail_limit
        result.gmail_response = gmail_response
        result.email = email
        result.invalid_email = invalid_email
        
        try:
            result.full_clean()
            result.save()
        except ValidationError:
            traceback.print_exc()

    # Update Gmass campaign report last accessed timestamp
    sgtz = pytz.timezone(TIME_ZONE)
    gmass_campaign.report_last_accessed = datetime.datetime.now(sgtz)
    gmass_campaign.save()