from django.contrib import admin

from .models import Card


class CardsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'type', 'bank', 'get_balance')
    list_filter = ('bank__name', 'type')


admin.site.register(Card, CardsAdmin)
