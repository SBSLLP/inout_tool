from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError    
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .form import CustomUserCreationForm
from .models import Attendance

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()

   
    try:
        attendance = Attendance.objects.get(user=request.user, check_out_time__isnull=True)
    except Attendance.DoesNotExist:
        attendance = None

  
    if request.method == "POST":
        if 'check_in' in request.POST:
            if not attendance:
               
                role = 'SBS_RESOURS'  
                Attendance.objects.create(user=request.user, check_in_time=timezone.now(), role=role)

        elif 'check_out' in request.POST:
            if attendance:
                attendance.check_out_time = timezone.now()
                attendance.save()

  
    daily_records = Attendance.objects.filter(user=user, date=today)

    return render(request, 'dashboard.html', {
        'attendance': attendance,
        'daily_records': daily_records
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method =="post":
        email=request.post['email']
        password=request.post['password']
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(dashboard.html)
        else:
            return render(request, 'login.html',{'error': 'Invalid email or password'})
    return redirect (request,'login.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'This email is already registered.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/dashboard/')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password.html', {'form': form})