import re
from django.db.models import QuerySet

from cards.models import Card
from emails.email_parsers.BaseEmailParser import BaseEmailParser
from transactions.models import Transaction


class IndusindCCParser(BaseEmailParser):

    def __init__(self, subject: str, email: str, cards: QuerySet(Card), transaction: Transaction):
        if 'Transaction Alert - IndusInd Bank Credit Card' not in subject:
            return

        result = re.findall("Card\sending\s(.+?)\sfor\sINR(.+?)\son\s(.+?)\sat\s(.+?)\sis\s(.+?)\.", email)
        if len(result) == 0:
            result = re.findall("Card\sending\s(.+?)\sfor\sINR\s(.+?)on\s(.+?)\sat\s(.+?)\sis\s(.+?)\.", email)

        card_number = result[0][0]
        amount = int(float(result[0][1].replace(',', '')) * 100)
        platform = result[0][3]
        is_approved = result[0][4] == 'Approved'

        if is_approved is False:
            print("Transaction For Indusind Credit Card {} for amount was not approved".format(card_number, amount))
            return

        transaction.card = cards.filter(card_number__endswith=card_number).first()
        transaction.amount_in_paise = amount
        transaction.platform = platform

        super().__init__(transaction)
