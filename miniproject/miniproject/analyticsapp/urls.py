from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ProductPerformanceViewSet, SalesMetricsViewSet,
                    TradingMetricsViewSet)

router = DefaultRouter()
router.register(r'trading-metrics', TradingMetricsViewSet, basename='trading-metrics')
router.register(r'sales-metrics', SalesMetricsViewSet, basename='sales-metrics')
router.register(r'product-performance', ProductPerformanceViewSet, basename='product-performance')

urlpatterns = [
    path('', include(router.urls)),
]
