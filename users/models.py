from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('warden', 'Warden'),
    ('student', 'Student'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # for warden approval

    def __str__(self):
        return f"{self.user.username} ({self.role})"
