from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=250)
    carbs = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    calories = models.IntegerField(default=0)


class Consume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)


class HealthGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_calorie_goal = models.IntegerField(default=2000)
    carb_goal = models.FloatField(default=50)
    protein_goal = models.FloatField(default=50)
    fat_goal = models.FloatField(default=50)

    def __str__(self):
        return f"{self.user.username}'s Health Goal"