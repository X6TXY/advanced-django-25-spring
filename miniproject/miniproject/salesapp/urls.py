from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, PromotionViewSet, SalesOrderViewSet

router = DefaultRouter()
router.register(r'promotions', PromotionViewSet)
router.register(r'orders', SalesOrderViewSet, basename='salesorder')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]