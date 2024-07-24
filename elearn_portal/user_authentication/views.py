from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.urls import reverse


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    if user.user_type.type_name == 'Admin':
        return redirect(reverse('courses:admin_dashboard'))   # Redirect to courses/admin/
    elif user.user_type.type_name == 'Staff':
       return redirect(reverse('courses:staff_dashboard'))  # Redirect to courses/staff/
    elif user.user_type.type_name == 'Student':
        return redirect(reverse('courses:student_dashboard'))   # Redirect to courses/student/
    else:
        return redirect('login')  # Redirect to login if user type is unknown