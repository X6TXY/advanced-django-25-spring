from django import forms

from .models import Food, HealthGoal


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "carbs", "proteins", "fats", "calories"]


class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['daily_calorie_goal', 'carb_goal', 'protein_goal', 'fat_goal']