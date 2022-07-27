from relationships import models as relmods
from leads import models as lemods
from growth.models import Fibre2FashionSellingOffer

def run():
    print('start')
    limit = 10
    for o in Fibre2FashionSellingOffer.objects.all():
        print(o)
        user, _ = relmods.User.objects.get_or_create(email=o.email)
        lead = lemods.Lead.objects.create(
            author=user,
            body=o.description,
            lead_type='selling'
        )

        print('Created ' + str(lead))

        limit -= 1
        if limit < 0:
            break