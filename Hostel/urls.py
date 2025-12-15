from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),            # guest/login/signup at root
    path('hostel/', include('hostelapp.urls')),
    path('students/', include('students.urls')),
    path('payments/', include('payments.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
