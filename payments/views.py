from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.utils import role_required
from .models import Payment
from students.models import StudentProfile
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
@role_required(['student'])
def make_payment(request):
    sp = StudentProfile.objects.get(user_profile=request.user.userprofile)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        screenshot = request.FILES.get('screenshot')
        Payment.objects.create(student=sp, amount=amount, screenshot=screenshot, status='completed')
        messages.success(request, "Payment submitted for verification")
        return redirect('student_dashboard')
    payments = Payment.objects.filter(student=sp).order_by('-date')
    return render(request, 'payments/make_payment.html', {'payments': payments})

@login_required
@role_required(['warden'])
def mark_payment_done(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, student__hostel__warden=request.user.userprofile)
    payment.status = 'completed'
    payment.save()
    messages.success(request, f"✅ Payment from {payment.student.user_profile.user.username} marked as done.")
    return redirect('view_payments')
