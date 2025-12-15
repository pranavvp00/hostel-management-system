from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile','hostel','room','request_status')
    list_filter = ('request_status','hostel')
