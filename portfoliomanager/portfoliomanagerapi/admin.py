from django.contrib import admin

from portfoliomanagerapi.models import Stock, Portfolio, Trade

admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Trade)