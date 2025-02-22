from django.contrib import admin

from .models import ProductPerformance, SalesMetrics, TradingMetrics


@admin.register(TradingMetrics)
class TradingMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_volume', 'average_price',
        'number_of_trades', 'highest_price', 'lowest_price'
    ]
    list_filter = ['date']


@admin.register(SalesMetrics)
class SalesMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_revenue', 'total_discount',
        'number_of_orders', 'average_order_value'
    ]
    list_filter = ['date']


@admin.register(ProductPerformance)
class ProductPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'date', 'sales_quantity',
        'sales_revenue', 'trading_volume',
        'average_trading_price'
    ]
    list_filter = ['date', 'product']
    search_fields = ['product__name']
