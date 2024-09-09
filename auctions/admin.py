from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Bids)
