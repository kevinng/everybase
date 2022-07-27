from django.db.models import F
from relationships import models as relmods
from leads import models as lemods
from growth.models import Fibre2FashionSellingOffer

def run():
    print(f'Start porting F2F selling leads...')

    print('Even leads only...')
    for o in Fibre2FashionSellingOffer.objects.annotate(odd=F('id') % 2).filter(odd=False):
        print(o)
        if o.email is not None:
            user, _ = relmods.User.objects.get_or_create(email=o.email)
            if (o.title is not None and o.title.strip() != '') or (o.description is not None and o.description.strip() != ''):
                lead = lemods.Lead.objects.create(
                    author=user,
                    body=o.title + ' ' + o.description,
                    lead_type='selling'
                )

                print('Created ' + str(lead))

    print('Odd leads only...')
    for o in Fibre2FashionSellingOffer.objects.annotate(odd=F('id') % 2).filter(odd=True):
        print(o)
        if o.email is not None:
            user, _ = relmods.User.objects.get_or_create(email=o.email)
            if (o.title is not None and o.title.strip() != '') or (o.description is not None and o.description.strip() != ''):
                lead = lemods.Lead.objects.create(
                    author=user,
                    body=o.title + ' ' + o.description,
                    lead_type='selling'
                )

                print('Created ' + str(lead))