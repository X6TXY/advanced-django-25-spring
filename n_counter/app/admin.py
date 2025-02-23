from django.contrib import admin

from .models import Consume, Food

admin.site.register(Food)
admin.site.register(Consume)