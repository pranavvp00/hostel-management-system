from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.utils import role_required
from hostelapp.models import Hostel, MessMenu, HostelGallery,Notice,Room
from .models import StudentProfile
from django.contrib import messages


@login_required
@role_required(['student'])
def student_dashboard(request):
    profile = request.user.userprofile
    sp = StudentProfile.objects.get(user_profile=profile)

    # Mess menu for joined hostel
    mess_menu = MessMenu.objects.filter(hostel=sp.hostel) if sp.hostel else []

    # Notices for this student (both personal and from warden)
    notices = Notice.objects.filter(student=sp).order_by('-created_at') if sp else []

    # Hostel galleries grouped as a single snippet
    gallery_groups = []
    if sp.hostel:
        gallery_groups = [{
            'id': sp.hostel.id,
            'images': HostelGallery.objects.filter(hostel=sp.hostel)
        }]

    # All hostels available for request
    hostels = Hostel.objects.all()

    context = {
        'profile': sp,
        'mess_menu': mess_menu,
        'notices': notices,
        'gallery_groups': gallery_groups,
        'hostels': hostels,
    }

    return render(request, 'students/student_dashboard.html', context)

@login_required
@role_required(['student'])
def edit_profile(request):
    sp = StudentProfile.objects.get(user_profile=request.user.userprofile)

    if request.method == 'POST':
        sp.phone_number = request.POST.get('phone_number')
        sp.guardian_number = request.POST.get('guardian_number')
        sp.parent_name = request.POST.get('parent_name')
        sp.parent_phone = request.POST.get('parent_phone')
        sp.department = request.POST.get('department')
        sp.address = request.POST.get('address')

        # Update photo
        if 'photo' in request.FILES:
            sp.photo = request.FILES['photo']

        sp.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('student_dashboard')

    return render(request, 'students/edit_profile.html', {'profile': sp})

@login_required
@role_required(['student'])
def request_hostel(request, hostel_id):
    sp = StudentProfile.objects.get(user_profile=request.user.userprofile)
    hostel = get_object_or_404(Hostel, id=hostel_id)

    # Check hostel capacity
    if hostel.capacity <= 0:
        messages.error(request, "This hostel is full. Cannot send request.")
        return redirect('student_dashboard')

    # Already pending
    if sp.request_status == 'pending' and sp.hostel == hostel:
        messages.info(request, "You already have a pending request for this hostel.")
        return redirect('student_dashboard')

    # Already approved
    if sp.request_status == 'approved' and sp.hostel:
        messages.info(request, f"You are already assigned to {sp.hostel.name}.")
        return redirect('student_dashboard')

    # Assign hostel and mark pending
    sp.hostel = hostel
    sp.request_status = 'pending'
    sp.request_message = request.POST.get('message', '')
    sp.save()

    messages.success(request, f"Request sent successfully to {hostel.name}.")
    return redirect('student_dashboard')


from .models import StudentReport

@login_required
@role_required(['student'])
def send_report(request):
    student_profile = request.user.userprofile

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            StudentReport.objects.create(student=student_profile, message=message_text)
            messages.success(request, "Report sent to admin successfully!")
        else:
            messages.error(request, "Please enter a message before sending.")

        return redirect('student_dashboard')  # Stay on dashboard after sending

    # Optional: display a form if you want separate page
    return render(request, 'students/send_report.html')