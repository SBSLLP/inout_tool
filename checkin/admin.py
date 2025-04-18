from django.contrib import admin
from .models import Attendance, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import site

class CustomUserAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('role',)}),
    )
    list_display = UserAdmin.list_display + ('role',)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date','user', 'role', 'check_in_time', 'check_out_time')
    list_filter = ('role', 'date')
    search_fields = ('user__username', 'role')
    ordering = ('-date',)


