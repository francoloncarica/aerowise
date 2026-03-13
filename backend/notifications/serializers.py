from rest_framework import serializers
from .models import AlertSubscription


class AlertSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertSubscription
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertSubscription
        fields = [
            'email', 'name', 'phone',
            'origin_keywords', 'destination_keywords',
            'min_date', 'max_date', 'max_price_usd',
            'aircraft_categories', 'frequency',
        ]
