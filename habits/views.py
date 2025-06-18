from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Habit, HabitProgress, Achievement, UserProfile
from .forms import RegisterForm
from datetime import timedelta
from .constants import HABIT_OPTIONS, EMOJI_OPTIONS

def home(request):
    habits = Habit.objects.filter(public=True).select_related('user').only(
        'name', 'description', 'streak', 'public', 'emoji', 'user__username'
    )
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

    return render(request, 'habits/home.html', {"habits": habit_data})

@login_required
def habit_stats(request):
    habits = Habit.objects.filter(user=request.user)
    
    stats = {
        'total_habits': habits.count(),
        'total_streak': sum(h.streak for h in habits),
        'best_streak': max(h.streak for h in habits) if habits else 0,
    }
    
    today = timezone.now().date()
    start_date = today - timedelta(days=30)
    
    progress = HabitProgress.objects.filter(
        habit__user=request.user,
        date__gte=start_date
    )
    
    completed = progress.filter(completed=True).count()
    total = progress.count()
    stats['completion_rate'] = completed / total * 100 if total > 0 else 0
    
    return render(request, 'habits/stats.html', {'stats': stats})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'habits/register.html', {'form': form})

@login_required
def dashboard(request):
    user_habits = Habit.objects.filter(user=request.user)
    achievements = Achievement.objects.all()
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    user_badges = profile.badges
    
    return render(request, 'habits/dashboard.html', {
        'habits': user_habits,
        'today': timezone.now().date(),
        'achievements': achievements,
        'user_badges': user_badges
    })

@login_required
def habit_create(request):
    if request.method == 'POST':
        custom_name = request.POST.get('custom_name')
        habit_name = request.POST.get('habit_name')
        habit_emoji = request.POST.get('habit_emoji')
        description = request.POST.get('custom_description', '')
        
        if custom_name:
            name = custom_name
            emoji = habit_emoji
        else: 
            name = habit_name
            emoji = habit_emoji
            
        if not name or not emoji:
            messages.error(request, "Nombre y emoji son requeridos")
            return redirect('habit_create')
            
        Habit.objects.create(
            name=name,
            description=description,
            user=request.user,
            emoji=emoji
        )
        
        check_achievements(request)
        
        return redirect('dashboard')
        
    return render(request, 'habits/habit_form.html', {
        'title': 'Crear Hábito',
        'habits': HABIT_OPTIONS,
        'emoji_options': EMOJI_OPTIONS,
    })

@login_required
def habit_toggle_visibility(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.public = not habit.public
    habit.save()
    return redirect('dashboard')


@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    if request.method == 'POST':
        custom_name = request.POST.get('custom_name')
        habit_name = request.POST.get('habit_name')
        habit_emoji = request.POST.get('habit_emoji')
        description = request.POST.get('custom_description', '')
        
        if custom_name:
            habit.name = custom_name
            habit.emoji = habit_emoji
        else: 
            habit.name = habit_name
            habit.emoji = habit_emoji
        
        habit.description = description
        habit.save()
        return redirect('dashboard')
    
    return render(request, 'habits/habit_form.html', {
        'title': 'Editar Hábito',
        'habits': HABIT_OPTIONS,
        'emoji_options': EMOJI_OPTIONS,
        'editing': True,
        'habit': habit,
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

    progress, created = HabitProgress.objects.update_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )
    
    if created or progress.completed:
        if habit.last_completed == today - timedelta(days=1):
            habit.streak += 1
        elif habit.last_completed != today:
            habit.streak = 1
        habit.last_completed = today
        habit.save()
        
        check_achievements(request, habit)

    return redirect('dashboard')

@login_required
def add_7_days_streak(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    
    for i in range(7):
        date = today - timedelta(days=i)
        HabitProgress.objects.update_or_create(
            habit=habit,
            date=date,
            defaults={'completed': True}
        )
    
    habit.streak = max(habit.streak, 7)
    habit.last_completed = today
    habit.save()
    
    return redirect('dashboard')

@login_required
def habit_toggle_progress(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()

    progress, created = HabitProgress.objects.update_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )
    
    if created or progress.completed:
        if habit.last_completed == today - timedelta(days=1):
            habit.streak += 1
        elif habit.last_completed != today:
            habit.streak = 1
        habit.last_completed = today
        habit.save()
        
        check_achievements(request, habit)

    return redirect('dashboard')

def check_achievements(request, habit=None):
    user = request.user 
    profile, _ = UserProfile.objects.get_or_create(user=user)
    achievements = Achievement.objects.all()
    unlocked_achievements = []
    
    for achievement in achievements:
        if achievement.condition.startswith('streak_'):
            required_streak = int(achievement.condition.split('_')[1])
            if habit and habit.streak >= required_streak:
                if achievement.badge_value not in profile.badges:
                    profile.badges.append(achievement.badge_value)
                    unlocked_achievements.append(achievement.name)
        
        elif achievement.condition.startswith('habit_count_'):
            required_count = int(achievement.condition.split('_')[2])
            habit_count = Habit.objects.filter(user=user).count()
            if habit_count >= required_count:
                if achievement.badge_value not in profile.badges:
                    profile.badges.append(achievement.badge_value)
                    unlocked_achievements.append(achievement.name)
    
    if unlocked_achievements:
        profile.save()
        for achievement_name in unlocked_achievements:
            messages.success(request, f'¡Logro desbloqueado: {achievement_name}!')