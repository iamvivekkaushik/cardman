from django.contrib import admin

from .models import Card


class CardsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'type', 'bank', 'is_active', 'get_balance')
    list_filter = ('bank__name', 'type', 'account_type', 'is_active')


admin.site.register(Card, CardsAdmin)
