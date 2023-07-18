import re
from django.db.models import QuerySet

from cards.models import Card
from emails.email_parsers.BaseEmailParser import BaseEmailParser
from transactions.models import Transaction


class IciciCCParser(BaseEmailParser):

    def __init__(self, subject: str, email: str, cards: QuerySet(Card), transaction: Transaction):
        transaction_type = ''
        card_number = ''
        amount = 0
        platform = ''

        if re.search('Payment\sof.+R\s.+\sreceived.+ICICI.+Card\s.+', subject) is not None:
            transaction_type = 'CR'
            result = re.findall("of.+INR\s(.+?)\sto.+Card\s(.+?)\sh.+h\s(.+?)\s", email)
            amount = int(float(result[0][0].replace(',', '')) * 100)
            card_number = result[0][1].replace('X', '')
            platform = result[0][2]
        elif 'Transaction alert for your ICICI Bank Credit Card' in subject:
            transaction_type = 'DR'
            result = re.findall("Card\s(.+?)\s.*of\sINR(.+?)\s.*Info:\s(.+?)\.", email)
            card_number = result[0][0].replace('X', '')
            amount = int(float(result[0][1].replace(',', '')) * 100)
            platform = result[0][2]
        else:
            return

        transaction.card = cards.filter(card_number__endswith=card_number).first()
        transaction.amount_in_paise = amount
        transaction.platform = platform
        transaction.transaction_type = transaction_type

        super().__init__(transaction)
