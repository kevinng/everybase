import traceback
import requests
import os
import csv
import io
import datetime
import pytz

from celery import Celery, shared_task
from scripts.shared import helpers
from django.core.exceptions import ValidationError

from everybase.settings import (TIME_ZONE, SYSTS_LAST_UPDATED_GMASS_BOUNCES,
    SYSTS_LAST_UPDATED_GMASS_UNSUBSCRIBES)

from relationships.shared import record_email
from growth.models import GmassCampaign, GmassCampaignResult, GmassEmailStatus
from common.models import SystemTimestamp

app = Celery()

def get_gmass_campaign_id(gmass_campaign):
    return gmass_campaign.report_url\
        .split('?')[-1]\
        .split('&')[0]\
        .split('=')[1]

def load_gmass_account_unsubscribes(gmass_campaign):
    """
    Note: we provide the campaign though we're requesting for account-level
    unsubscribes.
    """

    id = get_gmass_campaign_id(gmass_campaign)

    # Download CSV file as data (without materializing into file)
    download_url = \
        f'https://www.gmass.co/gmass/downloadcsvaction?C={id}&RT=ua'
    data = requests.get(download_url).json()['data']

    # Parse CSV file in-memory with StringIO
    reader = csv.DictReader(io.StringIO(data))

    for row in reader:
        email_or_domain = row.get('EmailAddressOrDomain', None)

        # Note: will be recorded as an invalid email if this is a domain and
        # not an email (but this is rare).
        (email, invalid_email) = record_email(email_or_domain)

        status, _ = GmassEmailStatus.objects.get_or_create(
            email=email,
            invalid_email=invalid_email
        )

        status.unsubscribed = True

        try:
            status.full_clean()
            status.save()
        except ValidationError:
            traceback.print_exc()

    # Update last updated system timestamp
    try:
        timestamp = SystemTimestamp.objects.get(
            key=SYSTS_LAST_UPDATED_GMASS_UNSUBSCRIBES)
    except SystemTimestamp.DoesNotExist:
        timestamp = SystemTimestamp(
            key=SYSTS_LAST_UPDATED_GMASS_UNSUBSCRIBES)

    sgtz = pytz.timezone(TIME_ZONE)
    timestamp.timestamp = datetime.datetime.now(sgtz)
    timestamp.full_clean()
    timestamp.save()

def load_gmass_account_bounces(gmass_campaign):
    """
    Note: we provide the campaign though we're requesting for account-level
    bounces.
    """

    id = get_gmass_campaign_id(gmass_campaign)

    # Download CSV file as data (without materializing into file)
    download_url = \
        f'https://www.gmass.co/gmass/downloadcsvaction?C={id}&RT=ba'
    data = requests.get(download_url).json()['data']

    # Parse CSV file in-memory with StringIO
    reader = csv.DictReader(io.StringIO(data))

    # Create/update Gmass email bounce status
    for row in reader:
        email_address = helpers.clean_string(row.get('EmailAddress', None))
        (email, invalid_email) = record_email(email_address)

        status, _ = GmassEmailStatus.objects.get_or_create(
            email=email,
            invalid_email=invalid_email
        )

        status.bounced = True
        status.bounce_reason = helpers.clean_string(row.get('BounceReason', None))

        try:
            status.full_clean()
            status.save()
        except ValidationError:
            traceback.print_exc()

    # Update last updated system timestamp
    try:
        timestamp = SystemTimestamp.objects.get(
            key=SYSTS_LAST_UPDATED_GMASS_BOUNCES)
    except SystemTimestamp.DoesNotExist:
        timestamp = SystemTimestamp(
            key=SYSTS_LAST_UPDATED_GMASS_BOUNCES)

    sgtz = pytz.timezone(TIME_ZONE)
    timestamp.timestamp = datetime.datetime.now(sgtz)
    timestamp.full_clean()
    timestamp.save()

def load_gmass_campaign_main_report(gmass_campaign):

    id = get_gmass_campaign_id(gmass_campaign)

    # Download CSV file as data (without materializing into file)
    download_url = \
        f'https://www.gmass.co/gmass/downloadcsvaction?C={id}&RT=m'
    data = requests.get(download_url).json()['data']

    # Parse CSV file in-memory with StringIO
    reader = csv.DictReader(io.StringIO(data))

    for row in reader:
        email_address = helpers.clean_string(row.get('emailaddress', None))

        (email, invalid_email) = record_email(email_address)

        result, _ = GmassCampaignResult.objects.get_or_create(
            email_address=email_address,
            gmass_campaign=gmass_campaign
        )

        result.first_name = helpers.clean_string(row.get('firstname', None))
        result.last_name = helpers.clean_string(row.get('lastname', None))
        result.name_1 = helpers.clean_string(row.get('name1', None))
        result.opens = helpers.clean_integer(row.get('Opens', None))
        result.clicks = helpers.clean_integer(row.get('Clicks', None))
        result.replied = helpers.clean_string(row.get('Replied', None))
        result.unsubscribed = helpers.clean_string(row.get('Unsubscribed', None))
        result.bounced = helpers.clean_string(row.get('Bounced', None))
        result.blocked = helpers.clean_string(row.get('Blocked', None))
        result.over_gmail_limit = helpers.clean_string(row.get('OverGmailLimit', None))
        result.gmail_response = helpers.clean_string(row.get('GmailResponse', None))
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
    gmass_campaign.full_clean()
    gmass_campaign.save()

@app.task
def update_gmass_data():
    """Update Gmass data for campaigns younger than 14 days old.
    """

    # Process rows younger than 14 days old
    sgtz = pytz.timezone(TIME_ZONE)
    campaigns = GmassCampaign.objects.filter(
        created__gte=datetime.datetime.now(sgtz) - datetime.timedelta(days=14))

    for campaign in campaigns:
        load_gmass_campaign_main_report(campaign)
        load_gmass_account_bounces(campaign)
        load_gmass_account_unsubscribes(campaign)