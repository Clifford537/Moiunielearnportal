from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserType

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all())

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)
