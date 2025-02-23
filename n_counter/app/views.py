from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import FoodForm, HealthGoalForm
from .models import Consume, Food, HealthGoal


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "app/register.html.html", {"form": form})

@login_required
def index(request):
    user = request.user

    health_goal, created = HealthGoal.objects.get_or_create(user=user)

    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        food_obj = Food.objects.get(name=food_consumed)
        consumed_obj = Consume(user=user, food_consumed=food_obj)
        consumed_obj.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()

    consumed_food = Consume.objects.filter(user=user)

    return render(request, 'app/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'health_goal': health_goal,
    })


@login_required
def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if consumed_food.user != request.user:
        return redirect('index')

    if request.method == 'POST':
        consumed_food.delete()
        return redirect('index')
    return render(request, 'app/delete.html')


@login_required
def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = FoodForm()
    return render(request, "app/add_food.html", {"form": form})

@login_required
def update_goals(request):
    goal, _ = HealthGoal.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = HealthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = HealthGoalForm(instance=goal)
    return render(request, "app/update_goals.html", {"form": form})


@login_required
def chart_data(request):
    consumed = Consume.objects.filter(user=request.user)
    goal, _ = HealthGoal.objects.get_or_create(user=request.user)

    data = {
        "labels": [c.food_consumed.name for c in consumed],
        "carbs": [c.food_consumed.carbs for c in consumed],
        "proteins": [c.food_consumed.proteins for c in consumed],
        "fats": [c.food_consumed.fats for c in consumed],
        "calories": [c.food_consumed.calories for c in consumed],

        "goal_carbs": goal.carb_goal,
        "goal_proteins": goal.protein_goal,
        "goal_fats": goal.fat_goal,
        "goal_calories": goal.daily_calorie_goal,
    }

    return JsonResponse(data)