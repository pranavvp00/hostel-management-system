from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                role = request.user.userprofile.role
            except:
                return redirect('login')
            if role not in allowed_roles:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
