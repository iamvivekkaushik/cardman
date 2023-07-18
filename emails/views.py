import json
import requests
import importlib
import base64
import mailparser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from banks.models import Bank
from cardman import request_parsers
from transactions.models import Transaction
from cards.models import Card
from .models import RegisteredEmail


def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


class InboundEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [request_parsers.PlainTextParser]

    @staticmethod
    def post(request):
        try:
            event = json.loads(request.data)

            if event.get('Type', '') == 'SubscriptionConfirmation':
                url = event.get('SubscribeURL', 'https://example.com')
                requests.get(url)
                return Response({"success": True}, status=status.HTTP_200_OK)

            if event.get('notificationType', '') != 'Received':
                return Response({"success": True}, status=status.HTTP_200_OK)

            user = RegisteredEmail.objects.get(email=event.get('mail', {}).get('source', '').lower()).user
            base64_message = event.get('content', '')
            decoded_bytes = base64.b64decode(base64_message)
            mail = mailparser.parse_from_bytes(decoded_bytes)
            decoded_message = ''
            for i in mail.text_plain:
                decoded_message += i
            if decoded_message == '':
                for i in mail.text_html:
                    decoded_message += i

            for bank in Bank.objects.all():
                if bank.alert_email in decoded_message.lower() or bank.alert_email in mail.headers['From'].lower():
                    parser = getattr(
                        importlib.import_module('emails.email_parsers.' + bank.cc_transaction_email_parser),
                        bank.cc_transaction_email_parser
                    )
                    transaction = Transaction()
                    parser(
                        mail.headers['Subject'],
                        strip_non_ascii(decoded_message).replace('\r\n', '').replace('=', '').replace('>', ''),
                        Card.objects.filter(user=user, bank=bank),
                        transaction
                    )
                    return Response({"success": True}, status=status.HTTP_200_OK)

            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
        return Response({"success": True}, status=status.HTTP_200_OK)
