import pytz
from datetime import datetime
from growth import models

def run():
    sgtz = pytz.timezone('Asia/Singapore')

    models.ChemicalBookSupplier.objects.all().update(
        harvested=datetime(2020, 3, 8, tzinfo=sgtz))

    models.ChemicalClusterOfSingaporeCompany.objects.all().update(
        harvested=datetime(2020, 2, 28, tzinfo=sgtz))

    models.ChemicalClusterOfSingaporeProduct.objects.all().update(
        harvested=datetime(2020, 2, 28, tzinfo=sgtz))

    models.ChemicalClusterOfSingaporeService.objects.all().update(
        harvested=datetime(2020, 2, 28, tzinfo=sgtz))

    models.Fibre2FashionBuyingOffer.objects.all().update(
        harvested=datetime(2020, 3, 3, tzinfo=sgtz))

    models.Fibre2FashionSellingOffer.objects.all().update(
        harvested=datetime(2020, 2, 29, tzinfo=sgtz))

    models.LookChemSupplier.objects.all().update(
        harvested=datetime(2020, 3, 9, tzinfo=sgtz))

    models.OKChemBuyingRequest.objects.all().update(
        harvested=datetime(2020, 2, 24, tzinfo=sgtz))

    models.WorldOfChemicalsSupplier.objects.all().update(
        harvested=datetime(2020, 3, 8, tzinfo=sgtz))

    models.ZeroBounceResult.objects.all().update(
        generated=datetime(2020, 3, 9, tzinfo=sgtz))