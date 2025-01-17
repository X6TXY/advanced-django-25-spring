from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, PriorityViewSet, ProjectViewSet,
                    TaskViewSet, UserViewSet)

router = DefaultRouter()

router.register(r'users', UserViewSet)

router.register(r'projects', ProjectViewSet)

router.register(r'categories', CategoryViewSet)

router.register(r'priorities', PriorityViewSet)

router.register(r'tasks', TaskViewSet)

urlpatterns = router.urls
