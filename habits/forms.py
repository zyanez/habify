from django import forms
from .models import Habit
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-sage-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sage-300 bg-white text-sage-800 placeholder-sage-400'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-sage-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sage-300 bg-white text-sage-800 placeholder-sage-400',
                'rows': 4
            }),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-sage-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sage-300 bg-white text-sage-800 placeholder-sage-400'
            })

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-sage-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sage-300 bg-white text-sage-800 placeholder-sage-400'
            })