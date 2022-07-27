from relationships import models as relmods
from leads import models as lemods
from growth.models import Fibre2FashionSellingOffer

def run():
    limit = 10
    for o in Fibre2FashionSellingOffer.objects.all():
        user, _ = relmods.User.objects.get_or_create(email=o.email)
        lead = lemods.Lead.objects.create(
            author=user,
            body=o.description
        )

        print('Created ' + str(lead))

        limit -= 1
        if limit < 0:
            break