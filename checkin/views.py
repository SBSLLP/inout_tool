from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Attendance

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()

    # Check if the user has already checked in
    try:
        attendance = Attendance.objects.get(user=request.user, check_out_time__isnull=True)
    except Attendance.DoesNotExist:
        attendance = None

    # Handle check-in/check-out
    if request.method == "POST":
        if 'check_in' in request.POST:
            if not attendance:
                # If role is missing, set it to "Staff"
                role = 'SBS_RESOURS'  # You can dynamically change this as per your requirement
                Attendance.objects.create(user=request.user, check_in_time=timezone.now(), role=role)

        elif 'check_out' in request.POST:
            if attendance:
                attendance.check_out_time = timezone.now()
                attendance.save()

    # Fetch daily attendance records
    daily_records = Attendance.objects.filter(user=user, date=today)

    return render(request, 'dashboard.html', {
        'attendance': attendance,
        'daily_records': daily_records
    })

def logout_view(request):
    logout(request)
    return redirect('login')

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
