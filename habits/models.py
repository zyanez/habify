from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    THEME_CHOICES = [
        ('light', 'Claro'),
        ('dark', 'Oscuro'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    badges = models.JSONField(default=list, blank=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    theme_expires = models.DateField(null=True, blank=True)
    is_highlighted = models.BooleanField(default=False)
    highlight_expires = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    streak = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    emoji = models.CharField(max_length=10, default="🌱")

    def __str__(self):
        return self.name
    
    @property
    def completed_today(self):
        return HabitProgress.objects.filter(
            habit=self, 
            date=timezone.now().date(), 
            completed=True
        ).exists()

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.name} on {self.date}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(max_length=50)
    badge_value = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name