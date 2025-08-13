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

    def __str__(self):
        return "{0} ({1})".format(self.card_number[-4:], self.bank.name)
