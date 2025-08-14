from rest_framework import serializers
from django.utils import timezone

from cards.models import *


class CardSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ["id", "card_number", "bank", "is_active", "account_type", "is_paid", "bank_name", "balance"]

    def get_balance(self, obj):
        return obj.get_balance()

    def get_bank_name(self, obj):
        return obj.bank.name


class CardAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ["user", ]

class CardBillingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["due_date", "credit_limit", "reward_points", "last_bill_amount"]
    
    def update(self, instance, validated_data):
        # Set billed_at to current timestamp
        instance.billed_at = timezone.now()
        if validated_data.get('last_bill_amount') > 0:
            instance.is_paid = False
        else:
            instance.is_paid = True
        
        # Update the other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
