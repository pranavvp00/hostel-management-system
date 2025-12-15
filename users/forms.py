from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# -----------------------------
# Helper Validators
# -----------------------------

# Gmail-only validation
def validate_gmail(value):
    if not value.lower().endswith("@gmail.com"):
        raise ValidationError("Only Gmail addresses are allowed.")

# Strong password validation
def validate_strong_password(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(ch.isdigit() for ch in value):
        raise ValidationError("Password must contain at least one number.")
    if not any(ch.isalpha() for ch in value):
        raise ValidationError("Password must contain at least one letter.")
    if not any(ch in "!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~" for ch in value):
        raise ValidationError("Password must contain at least one special character.")

# Phone validator (10 digits)
phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid 10-digit phone number starting with 6-9."
)

# ----------------------------------------------------------
#                  STUDENT SIGNUP FORM
# ----------------------------------------------------------

class StudentSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(validators=[validate_gmail])
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_strong_password])
    phone = forms.CharField(max_length=20, validators=[phone_validator])
    address = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)
    parent_name = forms.CharField(max_length=150)
    parent_phone = forms.CharField(max_length=20, validators=[phone_validator])
    department = forms.CharField(max_length=100)

    # Validate Username Unique
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Validate Email Unique
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email


# ----------------------------------------------------------
#                  WARDEN SIGNUP FORM
# ----------------------------------------------------------

class WardenSignupForm(forms.Form):
    hostel_name = forms.CharField(max_length=200)
    warden_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(validators=[validate_gmail])
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_strong_password])
    phone = forms.CharField(max_length=20, validators=[phone_validator])
    address = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=200)
    capacity = forms.IntegerField(min_value=1, error_messages={"min_value": "Capacity must be at least 1."})
    room_rent = forms.DecimalField(max_digits=8, decimal_places=2)
    profile_photo = forms.ImageField(required=False)

    # Username Unique
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Email Unique
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email


# ----------------------------------------------------------
#                  LOGIN FORM
# ----------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
