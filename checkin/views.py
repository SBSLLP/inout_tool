from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def dashboard(request):
    try:
        attendance = Attendance.objects.get(user=request.user, check_out_time__isnull=True)
    except Attendance.DoesNotExist:
        attendance = None

    if request.method == "POST":
        if 'check_in' in request.POST:
            if not attendance:
                Attendance.objects.create(user=request.user, check_in_time=timezone.now())

        elif 'check_out' in request.POST:
           
            if attendance:
                attendance.check_out_time = timezone.now()
                attendance.save()

    # Set break time display 
    break_time_display = "00:00"  # Default if no break has been taken

    return render(request, 'dashboard.html', {'attendance': attendance, 'break_time_display': break_time_display})

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
