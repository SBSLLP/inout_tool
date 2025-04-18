from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Fullstack_developer', 'Fullstack_developer'),
        ('manager', 'Manager'),
        ('intern', 'intern'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SBS_RESOURCE')

    def __str__(self):
        return self.username

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=50, blank=True)  
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user.id}) - {self.check_in_time} to {self.check_out_time or 'Still Checked In'}"

    
