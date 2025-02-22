from rest_framework import serializers

from .models import ProductPerformance, SalesMetrics, TradingMetrics


class TradingMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingMetrics
        fields = '__all__'


class SalesMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesMetrics
        fields = '__all__'


class ProductPerformanceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductPerformance
        fields = [
            'id', 'product', 'product_name', 'date',
            'sales_quantity', 'sales_revenue',
            'trading_volume', 'average_trading_price'
        ]
