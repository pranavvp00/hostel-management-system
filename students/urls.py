from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    
    path('request-hostel/<int:hostel_id>/', views.request_hostel, name='request_hostel'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('send-report/', views.send_report, name='send_report'), 
]
