from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet, OrderBookViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orderbook', OrderBookViewSet, basename='orderbook')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
