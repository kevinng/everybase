from django.contrib import admin
from .models import (GmassCampaignResult, GmassCampaign,
    ChemicalClusterOfSingaporeResult, Fibre2FashionResult, ZeroBounceResult,
    DataSource, SourcedEmail)

admin.site.register(GmassCampaignResult)
admin.site.register(GmassCampaign)
admin.site.register(ChemicalClusterOfSingaporeResult)
admin.site.register(Fibre2FashionResult)
admin.site.register(ZeroBounceResult)
admin.site.register(DataSource)
admin.site.register(SourcedEmail)