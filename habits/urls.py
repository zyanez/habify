from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='habits/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('habit/create/', views.habit_create, name='habit_create'),
    path('habit/<int:pk>/edit/', views.habit_edit, name='habit_edit'),
    path('habit/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habits/<int:pk>/toggle/', views.habit_toggle_progress, name='habit_toggle_progress'),
    path('habit/<int:pk>/toggle_visibility/', views.habit_toggle_visibility, name='habit_toggle_visibility'),
    path('habit/<int:pk>/add_7_days/', views.add_7_days_streak, name='add_7_days_streak'),
]