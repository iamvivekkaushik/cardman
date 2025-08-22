from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from cards.choices import CARD_ACCOUNT_CHOICES, CARD_TYPE_CHOICES, CREDIT_CARD, VISA


class Card(models.Model):
    card_number = models.CharField(verbose_name=_("Card Number"), max_length=16, unique=True)
    name = models.CharField(max_length=40, default="")
    expiry = models.CharField(max_length=5, null=True)
    cvv = models.CharField(verbose_name=_("CVV"), max_length=3, null=True)
    account_type = models.CharField(max_length=2, choices=CARD_ACCOUNT_CHOICES, default=CREDIT_CARD)
    type = models.CharField(max_length=4, choices=CARD_TYPE_CHOICES, default=VISA)
    is_paid = models.BooleanField(verbose_name=_("Is Paid"), default=False)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bank = models.ForeignKey('banks.Bank', on_delete=models.CASCADE)
    due_date = models.DateField(verbose_name=_("Due Date"), null=True, blank=True)
    credit_limit = models.DecimalField(verbose_name=_("Credit Limit"), max_digits=15, decimal_places=2, default=0.00)
    reward_points = models.IntegerField(verbose_name=_("Reward Points"), default=0)
    last_bill_amount = models.IntegerField(verbose_name=_("Last Bill Amount"), default=0)
    billed_at = models.DateTimeField(verbose_name=_("Billed At"), null=True, blank=True)
    updated_at = models.DateTimeField(_("Modified At"), auto_now=True)

    def get_balance(self):
        cr_sum = self.transaction_set.filter(transaction_type='CR').aggregate(Sum('amount_in_paise'))[
                     'amount_in_paise__sum'] or 0
        dr_sum = self.transaction_set.filter(transaction_type='DR').aggregate(Sum('amount_in_paise'))[
                     'amount_in_paise__sum'] or 0
        return (cr_sum - dr_sum) / 100

    def get_outstanding_amount_paise(self):
        """
        Calculate outstanding amount in paise from transactions between 2nd last and last billed date (inclusive of start).
        The 2nd last billing date is the same day of the previous month as billed_at.
        Credit transactions are added, Debit transactions are subtracted.
        Returns the amount in paise (same logic as admin outstanding_amount function).
        """
        if not self.billed_at:
            return 0
        
        billed_at = self.billed_at
        year = billed_at.year
        if billed_at.month > 1:
            month = billed_at.month - 1
        else:
            month = 12
            year = year - 1
        day = billed_at.day
        
        second_last_billed_at = billed_at.replace(year=year, month=month, day=day)
        transactions = self.transaction_set.filter(time__gte=second_last_billed_at, time__lt=self.billed_at)
        credit_total = transactions.filter(transaction_type='CR').aggregate(
            total=Sum('amount_in_paise')
        )['total'] or 0
        debit_total = transactions.filter(transaction_type='DR').aggregate(
            total=Sum('amount_in_paise')
        )['total'] or 0
        outstanding_paise = credit_total - debit_total
        outstanding_paise = outstanding_paise * -1
        return outstanding_paise

    def __str__(self):
        return "{0} ({1})".format(self.card_number[-4:], self.bank.name)

    def save(self, *args, **kwargs):
        """
        Override save method to create payment transaction when is_paid changes to True.
        """
        # Check if this is an update (not a new object)
        if self.pk:
            try:
                old_instance = Card.objects.get(pk=self.pk)
                # Check if is_paid changed from False to True
                if not old_instance.is_paid and self.is_paid:
                    # Check outstanding amount
                    outstanding_paise = self.get_outstanding_amount_paise()

                    if outstanding_paise > 0:
                        # Save first to ensure the card state is updated
                        super().save(*args, **kwargs)
                        
                        # Import here to avoid circular imports
                        from transactions.models import Transaction
                        from django.utils import timezone
                        
                        # Create payment transaction
                        Transaction.objects.create(
                            amount_in_paise=self.last_bill_amount,
                            time=timezone.now(),
                            platform="System",
                            description=f"Marked as paid",
                            card=self,
                            transaction_type='CR'  # Credit transaction for payment
                        )
                        return  # Exit early since we already saved
                        
            except Card.DoesNotExist:
                pass  # Handle edge case where card doesn't exist
        
        # Default save behavior
        super().save(*args, **kwargs)
