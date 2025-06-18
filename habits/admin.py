from django.contrib import admin
from .models import Habit, HabitProgress

admin.site.register(Habit)
admin.site.register(HabitProgress)
