from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Habit, HabitProgress, Reward
from .forms import HabitForm, RegisterForm
from django.contrib.auth.models import User
from datetime import timedelta

def home(request):
    habits = Habit.objects.select_related('user').all()
    habit_data = []

    for habit in habits:
        streak = habit.streak
        if streak >= 21:
            emoji = "🌳"
        elif streak >= 14:
            emoji = "🌲"
        elif streak >= 7:
            emoji = "🌿"
        elif streak >= 3:
            emoji = "🌱"
        else:
            emoji = "🌰"

        habit_data.append({
            "habit": habit,
            "emoji": emoji,
            "streak": streak,
            "owner": habit.user.username,
        })

    return render(request, 'habits/home.html', {
        "habits": habit_data
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            print("error")
    else:
        form = RegisterForm()
    return render(request, 'habits/register.html', {'form': form})

@login_required
def dashboard(request):
    user_habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    return render(request, 'habits/dashboard.html', {
        'habits': user_habits,
        'today': today,
    })

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('dashboard')
        else:
            print("error")
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {
        'form': form,
        'title': 'Crear Hábito'
    })

@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print("error")
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {
        'form': form,
        'title': 'Editar Hábito'
    })

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Hábito eliminado correctamente.')
        return redirect('dashboard')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})

@login_required
def habit_toggle_progress(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()

    progress, created = HabitProgress.objects.get_or_create(habit=habit, date=today)
    if not progress.completed:
        progress.completed = True
        progress.save()

        if habit.last_completed == today - timedelta(days=1):
            habit.streak += 1
        elif habit.last_completed != today:
            habit.streak = 1
        habit.last_completed = today
        habit.save()
    else:
        print("error")

    return redirect('dashboard')



@login_required
def habit_reset_streak(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.streak = 0
    habit.save()
    return redirect('dashboard')

