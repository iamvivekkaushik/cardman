from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from cards.choices import CARD_TYPE_CHOICES, VISA


class Card(models.Model):
    card_number = models.CharField(verbose_name=_("Card Number"), max_length=16, unique=True)
    name = models.CharField(max_length=40, default="")
    expiry = models.CharField(max_length=5, null=True)
    cvv = models.CharField(verbose_name=_("CVV"), max_length=3, null=True)
    type = models.CharField(max_length=4, choices=CARD_TYPE_CHOICES, default=VISA)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bank = models.ForeignKey('banks.Bank', on_delete=models.CASCADE)

    def get_balance(self):
        cr_sum = self.transaction_set.filter(transaction_type='CR').aggregate(Sum('amount_in_paise'))[
                     'amount_in_paise__sum'] or 0
        dr_sum = self.transaction_set.filter(transaction_type='DR').aggregate(Sum('amount_in_paise'))[
                     'amount_in_paise__sum'] or 0
        return (cr_sum - dr_sum) / 100

    def __str__(self):
        return "{0} ({1})".format(self.card_number[-4:], self.bank.name)
