from django.contrib import admin
from .models import Habit, HabitProgress, Reward

admin.site.register(Habit)
admin.site.register(HabitProgress)
admin.site.register(Reward)
