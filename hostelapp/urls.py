from django.urls import path
from . import views

urlpatterns = [
    # Public hostel detail (for students)
    path('detail/<int:pk>/', views.hostel_detail, name='hostel_detail'),

    # Warden dashboard & management
    path('warden-dashboard/', views.warden_dashboard, name='warden_dashboard'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('edit-mess-menu/', views.edit_mess_menu, name='edit_mess_menu'),
    path('send-notice/', views.send_notice, name='send_notice'),
    path('create-room/', views.create_room, name='create_room'),

    path('assign-room/<int:student_id>/', views.assign_room, name='assign_room'),
    # Student management actions
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('remove-student/<int:student_id>/', views.remove_student, name='remove_student'),
    

    # Hostel profile & gallery management
    path('edit-hostel-profile/', views.edit_hostel_profile, name='edit_hostel_profile'),
    path('hostel-gallery/', views.hostel_gallery, name='hostel_gallery'),
    path('delete-gallery-group/<int:group_id>/', views.delete_gallery_group, name='delete_gallery_group'),

    path('warden/payments/', views.view_payments, name='view_payments'),

    
]
