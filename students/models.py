from django.db import models
from users.models import UserProfile
from hostelapp.models import Hostel, Room

REQUEST_CHOICES = (('pending','Pending'),('approved','Approved'),('rejected','Rejected'))

class StudentProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    request_status = models.CharField(max_length=20, choices=REQUEST_CHOICES, default='pending')

    # Add these fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    guardian_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    parent_name = models.CharField(max_length=150)
    parent_phone = models.CharField(max_length=20)
    department = models.CharField(max_length=150, blank=True)
    request_message = models.TextField(blank=True)
    joined_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user_profile.user.username

from users.models import UserProfile  # ✅ Correct import

class StudentReport(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.student.user.username} on {self.created_at}"