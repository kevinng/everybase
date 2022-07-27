from relationships import models as relmods
from leads import models as lemods
from growth.models import Fibre2FashionSellingOffer

def run():
    print(f'Start porting {str(Fibre2FashionSellingOffer.objects.all().count())} F2F selling leads...')
    limit = 10
    for o in Fibre2FashionSellingOffer.objects.all():
        print(o)
        user, _ = relmods.User.objects.get_or_create(email=o.email)
        if (o.title is not None and o.title.strip() != '') or (o.description is not None and o.description.strip() != ''):
            lead = lemods.Lead.objects.create(
                author=user,
                body=o.title + ' ' + o.description,
                lead_type='selling'
            )

        print('Created ' + str(lead))

        # limit -= 1
        # if limit < 0:
        #     break