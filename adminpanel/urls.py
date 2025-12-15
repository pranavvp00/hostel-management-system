from django.urls import path
from . import views

urlpatterns = [
    # Admin dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Warden approval/rejection
    path('approve-warden/<int:profile_id>/', views.approve_warden, name='approve_warden'),
    path('reject-warden/<int:profile_id>/', views.reject_warden, name='reject_warden'),

    # Hostels
    path('view-hostels/', views.view_hostels, name='hostel_list'),  # For dashboard link
    path('delete-hostel/<int:hostel_id>/', views.delete_hostel, name='delete_hostel'),

    # Notices
    path('post-notice/', views.post_notice, name='post_notice'),

    # Students
    path('students/', views.view_all_students, name='student_list'),  # New view
    path('hostel/<int:hostel_id>/students/', views.hostel_students, name='hostel_students'),
]
