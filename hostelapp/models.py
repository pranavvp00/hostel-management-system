from django.db import models
from users.models import UserProfile


class Hostel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    warden = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, limit_choices_to={'role':'warden'})
    description = models.TextField(blank=True)
    room_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    main_image = models.ImageField(upload_to='hostel_main/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HostelGallery(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='hostel_gallery/')
    caption = models.CharField(max_length=255, blank=True)


class HostelGalleryGroup(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='gallery_groups')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class HostelGalleryImage(models.Model):
    group = models.ForeignKey(HostelGalleryGroup, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostel_gallery/')


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hostel.name} - {self.room_number}"


class MessMenu(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='menus')
    day = models.CharField(max_length=20)
    items = models.TextField()

    def __str__(self):
        return f"{self.hostel.name} - {self.day}"


class Notice(models.Model):
    # Use string reference to avoid circular import
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='notices')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notice for {self.student.user_profile.user.username}"
