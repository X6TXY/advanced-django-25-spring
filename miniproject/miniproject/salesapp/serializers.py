from rest_framework import serializers

from .models import Invoice, Promotion, SalesOrder, SalesOrderItem


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = [
            'id', 'product', 'quantity', 'unit_price',
            'promotion', 'discount_amount', 'final_price'
        ]
        read_only_fields = ['final_price']


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'customer', 'sales_rep', 'status',
            'total_amount', 'discount_amount', 'final_amount',
            'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['final_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sales_order = SalesOrder.objects.create(**validated_data)

        total_amount = 0
        total_discount = 0

        for item_data in items_data:
            quantity = item_data['quantity']
            unit_price = item_data['unit_price']
            promotion = item_data.get('promotion')

            item_total = quantity * unit_price
            item_discount = 0

            if promotion and promotion.is_active:
                item_discount = (item_total * promotion.discount_percentage / 100)
            total_amount += item_total
            total_discount += item_discount
            SalesOrderItem.objects.create(
                sales_order=sales_order,
                discount_amount=item_discount,
                final_price=item_total - item_discount,
                **item_data
            )

        sales_order.total_amount = total_amount
        sales_order.discount_amount = total_discount
        sales_order.save()

        return sales_order


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id', 'sales_order', 'invoice_number',
            'pdf_file', 'generated_at', 'due_date',
            'payment_status'
        ]
        read_only_fields = ['invoice_number', 'pdf_file', 'generated_at']
