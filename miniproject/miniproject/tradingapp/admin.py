from django.contrib import admin

from .models import Notification, Order, OrderBook, Transaction


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'order_type', 'quantity', 'price', 'status', 'created_at']
    list_filter = ['order_type', 'status', 'created_at']
    search_fields = ['user__username', 'product__name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'buy_order', 'sell_order', 'quantity', 'price', 'executed_at']
    list_filter = ['executed_at']
    search_fields = ['buy_order__user__username', 'sell_order__user__username']


@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'read', 'created_at']
    list_filter = ['notification_type', 'read', 'created_at']
    search_fields = ['user__username', 'message']
