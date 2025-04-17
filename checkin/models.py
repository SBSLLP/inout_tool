from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Developer', 'Developer'),
        ('Manager', 'Manager'),
        ('Designer', 'Designer'),
        ('Intern', 'intern'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=50, blank=True)  
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.user.id}) - {self.check_in_time} to {self.check_out_time or 'Still Checked In'}"

    def working_duration(self):
        if self.check_out_time:
            return self.check_out_time - self.check_in_time
        return timedelta(0)

    def save(self, *args, **kwargs):
        # Auto-fill role from UserProfile if not provided
        if not self.role:
            profile = UserProfile.objects.filter(user=self.user).first()
            if profile:
                self.role = profile.role
        super().save(*args, **kwargs)
