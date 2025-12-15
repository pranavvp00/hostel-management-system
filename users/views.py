from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import StudentSignupForm, WardenSignupForm, LoginForm
from hostelapp.models import Hostel
from students.models import StudentProfile


# ----------------------------------------------------------
#                      UNIFIED LOGIN
# ----------------------------------------------------------

def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            # Profile check
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                messages.error(request, "Profile missing. Contact admin.")
                return redirect('user_login')

            role = profile.role

            # Warden must be approved by admin
            if role == 'warden' and not profile.is_approved:
                messages.error(request, "Your account is not approved by admin yet.")
                return redirect('user_login')

            # Login successful
            login(request, user)

            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'warden':
                return redirect('warden_dashboard')
            else:
                return redirect('student_dashboard')

        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'users/login.html', {'form': form})


# ----------------------------------------------------------
#                         LOGOUT
# ----------------------------------------------------------

def user_logout(request):
    logout(request)
    return redirect('guest_page')


# ----------------------------------------------------------
#                STUDENT SIGNUP (with validation)
# ----------------------------------------------------------

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST, request.FILES)

        if form.is_valid():  # All validation already handled in forms.py
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            profile = UserProfile.objects.create(
                user=user,
                role='student',
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data.get('address', ''),
                profile_photo=form.cleaned_data.get('profile_photo'),
                is_approved=True  # students are auto-approved
            )

            StudentProfile.objects.create(
                user_profile=profile,
                parent_name=form.cleaned_data['parent_name'],
                parent_phone=form.cleaned_data['parent_phone'],
                department=form.cleaned_data['department']
            )

            messages.success(request, "Registered successfully! Please log in.")
            return redirect('login')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = StudentSignupForm()

    return render(request, 'users/student_signup.html', {'form': form})


# ----------------------------------------------------------
#                 WARDEN SIGNUP (with validation)
# ----------------------------------------------------------

def warden_signup(request):
    if request.method == 'POST':
        form = WardenSignupForm(request.POST, request.FILES)

        if form.is_valid():   # All validation handled in forms.py

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            profile = UserProfile.objects.create(
                user=user,
                role='warden',
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                profile_photo=form.cleaned_data.get('profile_photo'),
                is_approved=False  # needs admin approval
            )

            Hostel.objects.create(
                name=form.cleaned_data['hostel_name'],
                location=form.cleaned_data['location'],
                capacity=form.cleaned_data['capacity'],
                warden=profile,
                description=f"Warden: {form.cleaned_data['warden_name']}",
                room_rent=form.cleaned_data['room_rent']
            )

            messages.success(request, "Warden registered. Wait for admin approval.")
            return redirect('login')

        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = WardenSignupForm()

    return render(request, 'users/warden_signup.html', {'form': form})


# ----------------------------------------------------------
#                      GUEST PAGE
# ----------------------------------------------------------

def guest_page(request):
    hostels = Hostel.objects.all()
    return render(request, 'users/landing.html', {'hostels': hostels})
