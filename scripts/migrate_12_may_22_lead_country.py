from leads import models

def run():
    for lead in models.Lead.objects.all():
        if lead.lead_type == 'buying' and lead.country is not None and lead.buy_country is None:
            lead.buy_country = lead.country
            lead.save()
            print('Updated %s ' % lead)
        elif lead.lead_type == 'selling' and lead.country is not None and lead.sell_country is None:
            lead.sell_country = lead.country
            lead.save()
            print('Updated %s ' % lead)