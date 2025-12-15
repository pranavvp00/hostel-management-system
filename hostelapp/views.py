from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.utils import role_required
from .models import Hostel, Room, HostelGallery, MessMenu, HostelGalleryImage, HostelGalleryGroup, Notice
from students.models import StudentProfile
from django.contrib import messages
from django.utils import timezone
from adminpanel.models import Notice as AdminNotice
from hostelapp.models import Notice as StudentNotice
from django.db.models import Q
from payments.models import Payment


# Hostel detail for students
def hostel_detail(request, pk):
    hostel = get_object_or_404(Hostel, pk=pk)
    return render(request, 'hostelapp/hostel_detail.html', {'hostel': hostel})

from django.db.models import F

@login_required
@role_required(['warden'])
def warden_dashboard(request):
    profile = request.user.userprofile
    if not profile.is_approved:
        messages.warning(request, "Your account is pending admin approval.")
        return render(request, 'hostelapp/warden_pending.html')

    hostel = Hostel.objects.filter(warden=profile).first()

    if hostel:
        rooms = Room.objects.filter(hostel=hostel)
        students = StudentProfile.objects.filter(hostel=hostel)
        pending_students = students.filter(request_status='pending')
        vacant_rooms = rooms.filter(is_occupied=False)
    else:
        rooms = []
        students = []
        pending_students = []
        vacant_rooms = []

    # Latest 5 admin notices
    admin_notices = AdminNotice.objects.all().order_by('-created_at')[:5]

    # Latest 5 **unique messages** for this hostel's students
    student_notices = (
        StudentNotice.objects.filter(student__hostel=hostel)
        .values('message', 'created_at')  # only unique messages
        .order_by('-created_at')[:5]
    )

    context = {
        'hostel': hostel,
        'rooms': rooms,
        'students': students,
        'pending_students_count': pending_students.count(),
        'vacant_rooms_count': vacant_rooms.count(),
        'admin_notices': admin_notices,
        'student_notices': student_notices,
    }

    return render(request, 'hostelapp/warden_dashboard.html', context)



@login_required
@role_required(['warden'])
def create_room(request):
    warden_profile = request.user.userprofile
    hostel = Hostel.objects.filter(warden=warden_profile).first()

    if request.method == "POST":
        room_number = request.POST.get("room_number")
        if room_number:
            Room.objects.create(hostel=hostel, room_number=room_number)
            messages.success(request, f"Room {room_number} created successfully.")
        else:
            messages.error(request, "Please enter a room number.")

        return redirect('create_room')

    return render(request, 'hostelapp/create_room.html', {'hostel': hostel})

# Assign room to student
@login_required
@role_required(['warden'])
def assign_room(request, student_id):
    sp = get_object_or_404(StudentProfile, id=student_id, hostel__warden=request.user.userprofile)
    hostel = sp.hostel

    if request.method == "POST":
        room_id = request.POST.get("room_id")
        room_number = request.POST.get("room_number")

        # Determine the room object
        if room_id:
            room = get_object_or_404(Room, id=room_id, hostel=hostel)
        elif room_number:
            try:
                room = Room.objects.get(hostel=hostel, room_number=room_number)
            except Room.DoesNotExist:
                messages.error(request, f"Room {room_number} does not exist in {hostel.name}.")
                return redirect('manage_students')
        else:
            messages.error(request, "Please select or type a room.")
            return redirect('manage_students')

        # Check if room is occupied
        if room.is_occupied:
            messages.error(request, f"Room {room.room_number} is already occupied.")
            return redirect('manage_students')

        # ✅ Assign room to student
        sp.room = room
        sp.request_status = 'approved'
        sp.joined_at = timezone.now()
        sp.save()  # Important! Must call save()

        # ✅ Mark room as occupied
        room.is_occupied = True
        room.save()

        messages.success(request, f"Room {room.room_number} assigned to {sp.user_profile.user.username}")
        return redirect('manage_students')

    return redirect('manage_students')



@login_required
@role_required(['warden'])
def remove_student(request, student_id):
    sp = get_object_or_404(StudentProfile, id=student_id, hostel__warden=request.user.userprofile)
    hostel = sp.hostel
    if hostel and sp.request_status == 'approved':
        hostel.capacity += 1  # increment capacity
        hostel.save()

    # Remove student from hostel
    sp.hostel = None
    sp.room = None
    sp.request_status = 'pending'  # reset to pending
    sp.save()

    messages.success(request, "Student removed and hostel capacity updated.")
    return redirect('manage_students')

@login_required
@role_required(['warden'])
def manage_students(request):
    warden_profile = request.user.userprofile
    hostel = Hostel.objects.filter(warden=warden_profile).first()

    if hostel:
        students = StudentProfile.objects.filter(hostel=hostel).order_by('request_status', 'user_profile__user__username')

        # Filter for assigned students
        query = request.GET.get('q', '')
        if query:
            students = students.filter(
                Q(room__room_number__icontains=query) |
                Q(user_profile__user__username__icontains=query)
            )
    else:
        students = StudentProfile.objects.none()

    return render(request, 'hostelapp/manage_students.html', {
        'hostel': hostel,
        'students': students,
        'search_query': request.GET.get('q', '')
    })


@login_required
@role_required(['warden'])
def edit_mess_menu(request):
    """View/edit the mess menu for the warden's hostel"""
    warden_profile = request.user.userprofile
    hostel = Hostel.objects.filter(warden=warden_profile).first()

    if not hostel:
        messages.error(request, "No hostel assigned to your profile.")
        return redirect('warden_dashboard')

    if request.method == 'POST':
        items = request.POST.get('items')
        day = request.POST.get('day')
        if items and day:
            MessMenu.objects.create(hostel=hostel, items=items, day=day)
            messages.success(request, "Mess menu updated.")
            return redirect('edit_mess_menu')

    menus = MessMenu.objects.filter(hostel=hostel)
    return render(request, 'hostelapp/edit_mess_menu.html', {'hostel': hostel, 'menus': menus})


@login_required
@role_required(['warden'])
def send_notice(request):
    """Warden sends notices to students in their hostel"""
    warden_profile = request.user.userprofile
    hostel = Hostel.objects.filter(warden=warden_profile).first()
    students = StudentProfile.objects.filter(hostel=hostel)

    if request.method == 'POST':
        message = request.POST.get('message')
        for student in students:
            Notice.objects.create(student=student, message=message)
        messages.success(request, "Notice sent to all students.")
        return redirect('warden_dashboard')

    return render(request, 'hostelapp/send_notice.html', {'hostel': hostel, 'students': students})


@login_required
@role_required(['warden'])
def edit_hostel_profile(request):
    """Edit hostel details"""
    hostel = Hostel.objects.filter(warden=request.user.userprofile).first()
    if request.method == 'POST':
        hostel.name = request.POST.get('name')
        hostel.location = request.POST.get('location')
        hostel.capacity = request.POST.get('capacity')
        hostel.room_rent = request.POST.get('room_rent')
        hostel.description = request.POST.get('description')
        if 'main_image' in request.FILES:
            hostel.main_image = request.FILES['main_image']
        hostel.save()
        messages.success(request, "Hostel profile updated")
        return redirect('warden_dashboard')
    return render(request, 'hostelapp/edit_hostel_profile.html', {'hostel': hostel})


@login_required
@role_required(['warden'])
def hostel_gallery(request):
    """Warden can upload multiple images under one caption (album) and view/delete them"""
    hostel = Hostel.objects.filter(warden=request.user.userprofile).first()

    if not hostel:
        messages.error(request, "No hostel assigned to your account.")
        return redirect('warden_dashboard')

    if request.method == 'POST':
        images = request.FILES.getlist('images')
        caption = request.POST.get('caption', '').strip()

        if not images:
            messages.error(request, "Please select at least one image.")
        else:
            # Create one group (album) for all images
            group = HostelGalleryGroup.objects.create(hostel=hostel, caption=caption)
            for img in images:
                HostelGalleryImage.objects.create(group=group, image=img)
            messages.success(request, f"{len(images)} image(s) uploaded under one caption.")
        return redirect('hostel_gallery')

    gallery_groups = HostelGalleryGroup.objects.filter(hostel=hostel).prefetch_related('images')
    return render(request, 'hostelapp/hostel_gallery.html', {'hostel': hostel, 'gallery_groups': gallery_groups})


@login_required
@role_required(['warden'])
def delete_gallery_group(request, group_id):
    group = get_object_or_404(HostelGalleryGroup, id=group_id, hostel__warden=request.user.userprofile)
    group.delete()
    messages.success(request, "Gallery album deleted successfully.")
    return redirect('hostel_gallery')


@login_required
@role_required(['warden'])
def delete_gallery_image(request, image_id):
    """Delete a specific image from the hostel gallery"""
    image = get_object_or_404(HostelGalleryImage, id=image_id, group__hostel__warden=request.user.userprofile)
    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('hostel_gallery')

from django.utils import timezone

@login_required
@role_required(['warden'])
def approve_student(request, student_id):
    sp = get_object_or_404(StudentProfile, id=student_id, hostel__warden=request.user.userprofile)

    if sp.request_status != 'approved':
        sp.request_status = 'approved'
        sp.joined_at = timezone.now()
        sp.save()

        # Decrement hostel capacity if available
        hostel = sp.hostel
        if hostel.capacity > 0:
            hostel.capacity -= 1
            hostel.save()

        # Optional: create a notice for student
        notice_msg = f"🎉 Welcome to {hostel.name}! Your request has been approved."
        Notice.objects.create(student=sp, message=notice_msg)

        messages.success(request, f"{sp.user_profile.user.username} approved and hostel capacity updated.")
    else:
        messages.info(request, "Student already approved.")

    return redirect('manage_students')

@login_required
@role_required(['warden'])
def view_payments(request):
    warden_profile = request.user.userprofile
    hostel = Hostel.objects.filter(warden=warden_profile).first()

    payments = []
    if hostel:
        payments = (
            Payment.objects
            .filter(student__hostel=hostel)
            .select_related('student__user_profile__user')  # ✅ correct chain
            .order_by('-date')
        )

    return render(request, 'hostelapp/view_payments.html', {
        'hostel': hostel,
        'payments': payments,
    })
