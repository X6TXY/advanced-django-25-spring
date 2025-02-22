from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from productsapp.models import Product
from usersapp.models import User


class Order(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    ORDER_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    PARTIALLY_FILLED = 'partially_filled'
    ORDER_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (PARTIALLY_FILLED, 'Partially Filled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)
    filled_quantity = models.PositiveIntegerField(default=0)
    remaining_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:  # New order
            self.remaining_quantity = self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_type.upper()} {self.quantity} {self.product.name} at {self.price}"


class Transaction(models.Model):
    buy_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buy_transactions')
    sell_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sell_transactions')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.quantity} at {self.price}"


class OrderBook(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_book_entries')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_book_entry')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-order__price', '-created_at']


class Notification(models.Model):
    TRADE_EXECUTION = 'trade_execution'
    ORDER_MATCH = 'order_match'
    ORDER_CANCEL = 'order_cancel'
    NOTIFICATION_TYPES = [
        (TRADE_EXECUTION, 'Trade Execution'),
        (ORDER_MATCH, 'Order Match'),
        (ORDER_CANCEL, 'Order Cancel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type}: {self.message[:50]}"


@receiver(post_save, sender=Transaction)
def create_transaction_notification(sender, instance, created, **kwargs):
    if created:
        # Notify buyer
        Notification.objects.create(
            user=instance.buy_order.user,
            notification_type=Notification.TRADE_EXECUTION,
            message=f"Buy order executed: {instance.quantity} {instance.buy_order.product.name} at {instance.price}"
        )
        # Notify seller
        Notification.objects.create(
            user=instance.sell_order.user,
            notification_type=Notification.TRADE_EXECUTION,
            message=f"Sell order executed: {instance.quantity} {instance.sell_order.product.name} at {instance.price}"
        )
