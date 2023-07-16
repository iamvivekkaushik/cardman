import json
from collections import OrderedDict

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from cardman.utils import validate_filter
from cards.models import Card
from transactions.serializers import *


class CardTransactionListView(ListAPIView):
    def get_queryset(self):
        return Transaction.objects.filter(card=Card.objects.get(id=self.kwargs["card_id"], user=self.request.user))

    serializer_class = CardTransactionSerializer


class AllTransactionListView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'time': ['exact', 'lte', 'gte'], 'transaction_type': ['exact'],
                        'amount_in_paise': ['exact', 'gte', 'lte']}
    serializer_class = AllTransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(card__in=Card.objects.filter(user=self.request.user))


class TransactionInfoView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'time': ['exact', 'lte', 'gte'], 'transaction_type': ['exact']}
    serializer_class = TransactionInfoSerializer

    def get_queryset(self):
        transactions = Transaction.objects.filter(card__in=Card.objects.filter(user=self.request.user))

        kwargs = self.request.query_params.dict()
        kwargs = validate_filter(Transaction, kwargs, ['transaction_type', 'amount_in_paise'])

        if kwargs.__len__() > 0:
            transactions = transactions.filter(**kwargs)

        return transactions

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        debit = queryset.filter(transaction_type='DR').aggregate(Sum('amount_in_paise'))['amount_in_paise__sum'] or 0
        credit = queryset.filter(transaction_type='CR').aggregate(Sum('amount_in_paise'))['amount_in_paise__sum'] or 0
        balance = (credit - debit) / 100

        # set data to serializer
        serializer = TransactionInfoSerializer(data={"debit": debit / 100, "credit": credit / 100, "balance": balance})
        serializer.is_valid(raise_exception=True)
        # return HttpResponse(json.dumps(), status=status.HTTP_200_OK)
        return Response(serializer.data)


class AddTransactionView(CreateAPIView):
    serializer_class = AddTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(card=Card.objects.get(id=self.request.data["card"], user=self.request.user))
