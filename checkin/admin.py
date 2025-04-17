from django.contrib import admin
from .models import Attendance, UserProfile
from django.contrib.admin.sites import site

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date','user', 'role', 'check_in_time', 'check_out_time',  'working_duration')
    list_filter = ('role', 'date')
    search_fields = ('user__username', 'role')
    ordering = ('-date',)


