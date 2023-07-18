from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('CR', 'Credit'),
        ('DR', 'Debit'),
    )
    amount_in_paise = models.IntegerField()
    time = models.DateTimeField(default=datetime.now)
    platform = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    card = models.ForeignKey('cards.Card', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=2, blank=False, choices=TRANSACTION_TYPE_CHOICES, default='DR')
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(int(self.time.timestamp()))+"_"+str(self.id)+"_"+self.transaction_type+"_"+self.platform+"_INR_"+str(self.amount_in_paise)+"_using_"+self.card.card_number
