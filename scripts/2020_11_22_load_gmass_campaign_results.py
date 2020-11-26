from growth import tasks
from common.tasks import send_email

def run():
    tasks.update_gmass_data()