from django.urls import path
from . import views

urlpatterns = [
    path('', views.guest_page, name='guest_page'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/warden/', views.warden_signup, name='warden_signup'),
]
