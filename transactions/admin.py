from django.contrib import admin

from .models import Transaction


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('amount_in_paise', 'transaction_type', 'merchant', 'card', 'time')
    list_filter = ('card__card_number', 'card__bank__name', 'transaction_type')


admin.site.register(Transaction, TransactionsAdmin)
