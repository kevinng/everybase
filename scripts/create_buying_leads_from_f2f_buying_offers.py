from relationships import models as relmods
from leads import models as lemods
from growth.models import Fibre2FashionBuyingOffer

def run():
    limit = 10
    for o in Fibre2FashionBuyingOffer.objects.all():
        print(o)
        user, _ = relmods.User.objects.get_or_create(email=o.email)
        if o.description is not None and o.description.strip() != '':
            lead = lemods.Lead.objects.create(
                author=user,
                body=o.description,
                lead_type='buying'
            )

        print('Created ' + str(lead))

        limit -= 1
        if limit < 0:
            break