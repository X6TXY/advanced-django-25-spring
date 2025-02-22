from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notification, Order, OrderBook, Transaction
from .serializers import (NotificationSerializer, OrderBookSerializer,
                          OrderSerializer, TransactionSerializer)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        self._process_order(order)

    @transaction.atomic
    def _process_order(self, new_order):
        # Find matching orders
        matching_orders = Order.objects.filter(
            product=new_order.product,
            status__in=[Order.PENDING, Order.PARTIALLY_FILLED],
            order_type='sell' if new_order.order_type == 'buy' else 'buy',
            price__lte=new_order.price if new_order.order_type == 'buy' else None,
            price__gte=new_order.price if new_order.order_type == 'sell' else None,
        ).exclude(user=new_order.user).order_by('price', 'created_at')

        for matching_order in matching_orders:
            if new_order.remaining_quantity == 0:
                break

            match_quantity = min(
                new_order.remaining_quantity,
                matching_order.remaining_quantity
            )

            # Create transaction
            transaction_price = matching_order.price
            Transaction.objects.create(
                buy_order=new_order if new_order.order_type == 'buy' else matching_order,
                sell_order=matching_order if new_order.order_type == 'buy' else new_order,
                quantity=match_quantity,
                price=transaction_price
            )

            # Update orders
            for order in [new_order, matching_order]:
                order.filled_quantity += match_quantity
                order.remaining_quantity -= match_quantity
                order.status = (
                    Order.COMPLETED if order.remaining_quantity == 0
                    else Order.PARTIALLY_FILLED
                )
                order.save()

    @swagger_auto_schema(
        responses={200: OrderSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter by product ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'order_type',
                openapi.IN_QUERY,
                description="Filter by order type (buy/sell)",
                type=openapi.TYPE_STRING,
                enum=['buy', 'sell']
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by order status",
                type=openapi.TYPE_STRING,
                enum=['pending', 'completed', 'cancelled', 'partially_filled']
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        product_id = request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        order_type = request.query_params.get('order_type')
        if order_type:
            queryset = queryset.filter(order_type=order_type)

        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: 'Order cancelled successfully'}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in [Order.COMPLETED, Order.CANCELLED]:
            order.status = Order.CANCELLED
            order.save()
            return Response({'message': 'Order cancelled successfully'})
        return Response(
            {'error': 'Cannot cancel completed or already cancelled order'},
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderBook.objects.all()

    @swagger_auto_schema(
        responses={200: OrderBookSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Filter by product ID",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        buy_orders = Order.objects.filter(
            product_id=product_id,
            order_type='buy',
            status__in=[Order.PENDING, Order.PARTIALLY_FILLED]
        ).order_by('-price')[:10]

        sell_orders = Order.objects.filter(
            product_id=product_id,
            order_type='sell',
            status__in=[Order.PENDING, Order.PARTIALLY_FILLED]
        ).order_by('price')[:10]

        return Response({
            'buy_orders': OrderSerializer(buy_orders, many=True).data,
            'sell_orders': OrderSerializer(sell_orders, many=True).data,
        })


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        self.get_queryset().update(read=True)
        return Response({'status': 'all notifications marked as read'})
