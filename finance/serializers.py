from rest_framework import serializers
from .models import SubscriptionPlan, WalletTransaction

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    feature_list = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'title', 'months', 'price', 'is_special', 'feature_list']

    def get_feature_list(self, obj):
        return [f.strip() for f in obj.features.split(',') if f.strip()]

class WalletTransactionSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = ['id', 'title', 'amount', 'transaction_type', 'formatted_date']

    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%Y/%m/%d - %H:%M")