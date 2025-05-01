
from django.db import models
from users.models import User
from django.db import models
from django.utils import timezone

class Event(models.Model):

    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ]
    title = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)    
    time = models.TimeField(default=timezone.now)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='offline')

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  

    def __str__(self):
        return f"{self.user.studentID} registered for {self.event.title}"



from django.db import models
from django.conf import settings
from .models import Event

class CheckIn(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} checked in for {self.event.title} at {self.check_in_time}"
