from django.db import models
from students.models import StudentProfile

class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    screenshot = models.ImageField(upload_to='payments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=(('pending','Pending'),('completed','Completed')), default='completed')
    note = models.TextField(blank=True)
    def __str__(self):
        return f"{self.student.user_profile.user.username} - {self.amount}"
