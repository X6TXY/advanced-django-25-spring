from django.db import models


class User(models.Model):

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField()

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):

        return self.name


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):

        return self.name


class Priority(models.Model):

    level = models.CharField(max_length=50)

    def __str__(self):
        return self.level


class Task(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)

    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    due_date = models.DateField()

    def __str__(self):

        return self.title
