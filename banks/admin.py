from django.contrib import admin

from .models import Bank


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'alert_email', 'cc_transaction_email_parser')


admin.site.register(Bank, BankAdmin)
