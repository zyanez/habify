from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    streak = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def completed_today(self):
        return HabitProgress.objects.filter(habit=self, date=timezone.now().date(), completed=True).exists()

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.name} on {self.date}"

class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    points_required = models.PositiveIntegerField()

    def __str__(self):
        return self.name
