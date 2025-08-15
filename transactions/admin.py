from django.contrib import admin

from .models import Transaction


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('amount', 'transaction_type', 'platform', 'card', 'card_name', 'time')
    list_filter = ('card__card_number', 'card__bank__name', 'transaction_type')

    def amount(self, obj):
        """
        Display transaction_amount converted from paise to rupees.
        """
        if obj.amount_in_paise is None:
            return "₹0.00"
        
        # Convert from paise to rupees
        amount_rupees = obj.amount_in_paise / 100

        # Format as currency
        return f"₹{amount_rupees:,.2f}"
    
    def card_name(self, obj):
        """
        Display the name of the card associated with this transaction.
        """
        return obj.card.name if obj.card and obj.card.name else "No Name"
    
    card_name.short_description = 'Card Name'
    card_name.admin_order_field = 'card__name'  # Allows column sorting


admin.site.register(Transaction, TransactionsAdmin)
