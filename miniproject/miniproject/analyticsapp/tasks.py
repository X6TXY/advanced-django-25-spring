from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from productsapp.models import Product

from .models import ProductPerformance, SalesMetrics, TradingMetrics


@shared_task
def calculate_daily_metrics():
    date = timezone.now().date()

    TradingMetrics.calculate_daily_metrics(date)
    SalesMetrics.calculate_daily_metrics(date)

    for product in Product.objects.all():
        ProductPerformance.calculate_daily_metrics(product, date)


@shared_task
def generate_weekly_report():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)
    trading_metrics = TradingMetrics.objects.filter(
        date__range=[start_date, end_date]
    )
    sales_metrics = SalesMetrics.objects.filter(
        date__range=[start_date, end_date]
    )

    from django.core.cache import cache
    cache.set('weekly_trading_metrics', trading_metrics, timeout=3600)
    cache.set('weekly_sales_metrics', sales_metrics, timeout=3600)


@shared_task
def update_product_metrics(product_id):
    product = Product.objects.get(id=product_id)
    date = timezone.now().date()
    ProductPerformance.calculate_daily_metrics(product, date)