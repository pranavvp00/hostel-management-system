from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.utils import role_required
from users.models import UserProfile
from hostelapp.models import Hostel
from adminpanel.models import Notice
from students.models import StudentReport
# Admin Dashboard

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    hostels = Hostel.objects.all()
    wardens = UserProfile.objects.filter(role='warden')
    students = UserProfile.objects.filter(role='student')

    # Fetch all student reports
    student_reports = StudentReport.objects.all().order_by('-created_at')

    return render(request, 'adminpanel/admin_dashboard.html', {
        'hostels': hostels,
        'wardens': wardens,
        'students': students,
        'student_reports': student_reports,  # pass reports to template
    })
# Approve Warden
@login_required
@role_required(['admin'])
def approve_warden(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id, role='warden')
    profile.is_approved = True
    profile.save()
    messages.success(request, f"Warden {profile.user.username} approved successfully.")
    return redirect('admin_dashboard')  # Redirect to list of wardens

# Reject Warden
@login_required
@role_required(['admin'])
def reject_warden(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id, role='warden')
    profile.user.delete()  # Deletes the Django User + UserProfile
    messages.success(request, "Warden rejected and deleted successfully.")
    return redirect('admin_dashboard')

# View all hostels
@login_required
@role_required(['admin'])
def view_hostels(request):
    hostels = Hostel.objects.all()
    return render(request, 'adminpanel/view_hostels.html', {'hostels': hostels})

# Delete hostel
@login_required
@role_required(['admin'])
def delete_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    hostel.delete()
    messages.success(request, f"Hostel '{hostel.name}' deleted successfully.")
    return redirect('admin_dashboard')

# Post Notice
@login_required
@role_required(['admin'])
def post_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        if title and message:
            Notice.objects.create(title=title, message=message, posted_by=request.user)
            messages.success(request, "Notice posted successfully.")
        else:
            messages.error(request, "Title and message are required.")
        return redirect('admin_dashboard')

    recent_notices = Notice.objects.all().order_by('-created_at')[:5]
    return render(request, 'adminpanel/post_notice.html', {'recent_notices': recent_notices})

# View students in a hostel
@login_required
@role_required(['admin'])
def hostel_students(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    students = hostel.studentprofile_set.all()  # Assuming StudentProfile has FK to Hostel
    return render(request, 'adminpanel/hostel_students.html', {
        'hostel': hostel,
        'students': students
    })

@login_required
@role_required(['admin'])
def view_all_students(request):
    students = UserProfile.objects.filter(role='student')
    return render(request, 'adminpanel/student_list.html', {'students': students})
