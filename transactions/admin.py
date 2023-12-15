from django.contrib import admin
from .models import (
    Offer,
    OfferDetails,
    OfferItem,
    SaleBill, 
    SaleItem,
    SaleBillDetails
)

admin.site.register(SaleBill)
admin.site.register(SaleItem)
admin.site.register(SaleBillDetails)
admin.site.register(Offer)
admin.site.register(OfferItem)
admin.site.register(OfferDetails)


