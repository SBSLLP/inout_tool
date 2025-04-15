from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    break_time = models.IntegerField(default=0)  # Time in minutes

    def __str__(self):
        return f"{self.user.username} ({self.user.id}) - {self.check_in_time} to {self.check_out_time or 'Still Checked In'}"
