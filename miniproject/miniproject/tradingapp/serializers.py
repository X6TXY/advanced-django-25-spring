from decimal import Decimal

from rest_framework import serializers

from .models import Notification, Order, OrderBook, Transaction


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'product', 'order_type', 'quantity',
            'price', 'status', 'filled_quantity', 'remaining_quantity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'filled_quantity', 'remaining_quantity']


class TransactionSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Transaction
        fields = ['id', 'buy_order', 'sell_order', 'quantity', 'price', 'executed_at']
        read_only_fields = ['executed_at']


class OrderBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBook
        fields = ['id', 'product', 'order', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'message', 'read', 'created_at']
        read_only_fields = ['notification_type', 'message', 'created_at']
