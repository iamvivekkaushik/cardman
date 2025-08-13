from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import *


class CardListView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'bank_name': ['exact'],
        'card_number': ['exact', 'endswith', 'startswith'],
        'account_type': ['exact'],
        'is_active': ['exact'],
        'is_paid': ['exact'],
    }
    
    def get_queryset(self):
        user = self.request.user
        return Card.objects.filter(user=user)

    serializer_class = CardSerializer


class CardAddView(CreateAPIView):
    serializer_class = CardAddSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
