from leads import models

def run():
    for lead in models.Lead.objects.all():
        if lead.commission_type == 'percentage':
            lead.min_commission_percentage = lead.max_commission_percentage / 2
            lead.save()
            print('Updated %s minimum commission percentage ' % lead)