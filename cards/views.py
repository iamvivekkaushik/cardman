from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class CardListView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'bank': ['exact'],
        'name': ['exact'],
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

class CardBillingUpdateView(UpdateAPIView):
    serializer_class = CardBillingUpdateSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Card.objects.filter(user=user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_card = serializer.save()
        
        # Return updated card data with additional fields for confirmation
        response_data = {
            'id': updated_card.id,
            'card_number': updated_card.card_number,
            'due_date': updated_card.due_date,
            'credit_limit': updated_card.credit_limit,
            'reward_points': updated_card.reward_points,
            'last_bill_amount': updated_card.last_bill_amount,
            'billed_at': updated_card.billed_at,
            'message': 'Card billing information updated successfully'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

