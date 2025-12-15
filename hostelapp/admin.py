from django.contrib import admin
from .models import Hostel, HostelGallery, Room, MessMenu

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name','location','capacity','warden')

admin.site.register(HostelGallery)
admin.site.register(Room)
admin.site.register(MessMenu)
