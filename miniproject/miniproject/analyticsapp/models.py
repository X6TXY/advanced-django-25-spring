from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg, Sum
from django.utils import timezone
from productsapp.models import Product
from salesapp.models import SalesOrder
from tradingapp.models import Transaction


class TradingMetrics(models.Model):
    date = models.DateField(unique=True)
    total_volume = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    average_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    number_of_trades = models.PositiveIntegerField(default=0)
    highest_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    lowest_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Trading Metrics for {self.date}"

    @classmethod
    def calculate_daily_metrics(cls, date=None):
        if date is None:
            date = timezone.now().date()

        daily_transactions = Transaction.objects.filter(
            executed_at__date=date
        )

        metrics, _ = cls.objects.get_or_create(date=date)

        if daily_transactions.exists():
            metrics.total_volume = daily_transactions.aggregate(
                total=Sum('quantity'))['total'] or 0
            metrics.average_price = daily_transactions.aggregate(
                avg=Avg('price'))['avg'] or 0
            metrics.number_of_trades = daily_transactions.count()
            metrics.highest_price = daily_transactions.aggregate(
                max=models.Max('price'))['max'] or 0
            metrics.lowest_price = daily_transactions.aggregate(
                min=models.Min('price'))['min'] or 0
            metrics.save()

        return metrics


class SalesMetrics(models.Model):
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    number_of_orders = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Sales Metrics for {self.date}"

    @classmethod
    def calculate_daily_metrics(cls, date=None):
        if date is None:
            date = timezone.now().date()

        daily_orders = SalesOrder.objects.filter(
            created_at__date=date,
            status='completed'
        )

        metrics, _ = cls.objects.get_or_create(date=date)

        if daily_orders.exists():
            metrics.total_revenue = daily_orders.aggregate(
                total=Sum('final_amount'))['total'] or 0
            metrics.total_discount = daily_orders.aggregate(
                total=Sum('discount_amount'))['total'] or 0
            metrics.number_of_orders = daily_orders.count()
            metrics.average_order_value = (
                metrics.total_revenue / metrics.number_of_orders
                if metrics.number_of_orders > 0 else 0
            )
            metrics.save()

        return metrics


class ProductPerformance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    sales_quantity = models.PositiveIntegerField(default=0)
    sales_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    trading_volume = models.PositiveIntegerField(default=0)
    average_trading_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ['product', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.product.name} Performance on {self.date}"

    @classmethod
    def calculate_daily_metrics(cls, product, date=None):
        if date is None:
            date = timezone.now().date()

        sales_items = product.sales_items.filter(
            sales_order__created_at__date=date,
            sales_order__status='completed'
        )

        trades = Transaction.objects.filter(
            buy_order__product=product,
            executed_at__date=date
        )

        metrics, _ = cls.objects.get_or_create(
            product=product,
            date=date
        )

        if sales_items.exists():
            metrics.sales_quantity = sales_items.aggregate(
                total=Sum('quantity'))['total'] or 0
            metrics.sales_revenue = sales_items.aggregate(
                total=Sum('final_price'))['total'] or 0

        if trades.exists():
            metrics.trading_volume = trades.aggregate(
                total=Sum('quantity'))['total'] or 0
            metrics.average_trading_price = trades.aggregate(
                avg=Avg('price'))['avg'] or 0

        metrics.save()
        return metrics
