import csv
import io
from datetime import datetime, timedelta

from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from .models import ProductPerformance, SalesMetrics, TradingMetrics
from .serializers import (ProductPerformanceSerializer, SalesMetricsSerializer,
                          TradingMetricsSerializer)


class BaseMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_date_range(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = datetime.now().date() - timedelta(days=30)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = datetime.now().date()
        return start_date, end_date


class TradingMetricsViewSet(BaseMetricsViewSet):
    serializer_class = TradingMetricsSerializer

    def get_queryset(self):
        start_date, end_date = self.get_date_range(self.request)
        return TradingMetrics.objects.filter(date__range=[start_date, end_date])

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        queryset = self.get_queryset()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Date', 'Total Volume', 'Average Price',
            'Number of Trades', 'Highest Price', 'Lowest Price'
        ])
        
        for metric in queryset:
            writer.writerow([
                metric.date,
                metric.total_volume,
                metric.average_price,
                metric.number_of_trades,
                metric.highest_price,
                metric.lowest_price
            ])
            
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=trading_metrics.csv'
        return response

class SalesMetricsViewSet(BaseMetricsViewSet):
    serializer_class = SalesMetricsSerializer
    
    def get_queryset(self):
        start_date, end_date = self.get_date_range(self.request)
        return SalesMetrics.objects.filter(date__range=[start_date, end_date])

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        queryset = self.get_queryset()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Date', 'Total Revenue', 'Total Discount',
            'Number of Orders', 'Average Order Value'
        ])
        
        for metric in queryset:
            writer.writerow([
                metric.date,
                metric.total_revenue,
                metric.total_discount,
                metric.number_of_orders,
                metric.average_order_value
            ])
            
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=sales_metrics.csv'
        return response


class ProductPerformanceViewSet(BaseMetricsViewSet):
    serializer_class = ProductPerformanceSerializer
    
    def get_queryset(self):
        start_date, end_date = self.get_date_range(self.request)
        queryset = ProductPerformance.objects.filter(
            date__range=[start_date, end_date]
        )
        
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
            
        return queryset

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        queryset = self.get_queryset()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Date', 'Product', 'Sales Quantity',
            'Sales Revenue', 'Trading Volume',
            'Average Trading Price'
        ])
        
        for metric in queryset:
            writer.writerow([
                metric.date,
                metric.product.name,
                metric.sales_quantity,
                metric.sales_revenue,
                metric.trading_volume,
                metric.average_trading_price
            ])
            
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=product_performance.csv'
        return response
