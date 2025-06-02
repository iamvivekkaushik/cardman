from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Card


class CardsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'type', 'bank', 'is_paid', 'updated_at')
    list_filter = ('bank__name', 'type', 'account_type', 'is_paid', 'is_active')

    readonly_fields = (
        'options',
        'updated_at'
    )

    actions = ['bulk_update_is_paid']

    def options(self, obj):
        btn_id = 'copy-card-no'
        return mark_safe(f"""
            <input text="text" id="{btn_id}" value="{obj.card_number}" style="position: absolute; top: -10000px">
            <a href="#" onclick="document.querySelector(\'#{btn_id}\').select(); document.execCommand(\'copy\');" class="addlink">Copy card number to clipboard</a>
            """
        )
    
    options.short_description = _('Options')

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, "Selected cards have been marked as paid.")
    mark_as_paid.short_description = "Mark selected cards as paid"

    def mark_as_unpaid(self, request, queryset):
        queryset.update(is_paid=False)
        self.message_user(request, "Selected cards have been marked as unpaid.")
    mark_as_unpaid.short_description = "Mark selected cards as unpaid"

admin.site.register(Card, CardsAdmin)
