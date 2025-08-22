from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Q

from .models import Card


class CardsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'is_paid', 'outstanding_amount', 'formatted_last_bill_amount', 'billed_at', 'due_date')
    list_filter = ('bank__name', 'type', 'account_type', 'is_paid', 'is_active')

    readonly_fields = (
        'options',
        'outstanding_amount',
        'formatted_last_bill_amount',
        'updated_at'
    )

    actions = ['mark_as_paid', 'mark_as_unpaid']

    def options(self, obj):
        btn_id = 'copy-card-no'
        return mark_safe(f"""
            <input text="text" id="{btn_id}" value="{obj.card_number}" style="position: absolute; top: -10000px">
            <a href="#" onclick="document.querySelector(\'#{btn_id}\').select(); document.execCommand(\'copy\');" class="addlink">Copy card number to clipboard</a>
            """
        )
    
    options.short_description = _('Options')

    def outstanding_amount(self, obj):
        return f"₹{(obj.get_outstanding_amount_paise()/100):,.2f}"
    
    outstanding_amount.short_description = _('Outstanding Amount')
    outstanding_amount.admin_order_field = 'outstanding_amount'  # Allows column sorting

    def formatted_last_bill_amount(self, obj):
        """
        Display last_bill_amount converted from paise to rupees.
        """
        if obj.last_bill_amount is None:
            return "₹0.00"
        
        # Convert from paise to rupees
        amount_rupees = obj.last_bill_amount / 100
        
        # Format as currency
        return f"₹{amount_rupees:,.2f}"
    
    formatted_last_bill_amount.short_description = _('Last Bill Amount')
    formatted_last_bill_amount.admin_order_field = 'last_bill_amount'  # Allows column sorting

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, "Selected cards have been marked as paid.")
    mark_as_paid.short_description = "Mark selected cards as paid"

    def mark_as_unpaid(self, request, queryset):
        queryset.update(is_paid=False)
        self.message_user(request, "Selected cards have been marked as unpaid.")
    mark_as_unpaid.short_description = "Mark selected cards as unpaid"

admin.site.register(Card, CardsAdmin)
