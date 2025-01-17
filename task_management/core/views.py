import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Category, Priority, Project, Task, User
from .serializers import (CategorySerializer, PrioritySerializer,
                          ProjectSerializer, TaskSerializer, UserSerializer)

logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer


class ProjectViewSet(ModelViewSet):

    queryset = Project.objects.all()

    serializer_class = ProjectSerializer


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer


class PriorityViewSet(ModelViewSet):

    queryset = Priority.objects.all()

    serializer_class = PrioritySerializer


class TaskViewSet(ModelViewSet):

    queryset = Task.objects.all()

    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'priority', 'category']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        logger.info(f"Creating task: {serializer.validated_data}")
        serializer.save()
