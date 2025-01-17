from rest_framework import serializers

from .models import Category, Priority, Project, Task, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Project

        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = '__all__'


class PrioritySerializer(serializers.ModelSerializer):

    class Meta:

        model = Priority

        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = Task

        fields = '__all__'
