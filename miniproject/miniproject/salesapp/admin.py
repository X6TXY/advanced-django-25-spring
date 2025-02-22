from django.contrib import admin

from .models import Invoice, Promotion, SalesOrder, SalesOrderItem


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percentage', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['products']


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'sales_rep', 'status', 'total_amount', 'final_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__username', 'sales_rep__username']
    inlines = [SalesOrderItemInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'sales_order', 'generated_at', 'due_date', 'payment_status']
    list_filter = ['payment_status', 'generated_at', 'due_date']
    search_fields = ['invoice_number', 'sales_order__customer__username']
