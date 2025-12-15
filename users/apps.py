from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_admin(sender, **kwargs):
    from django.contrib.auth import get_user_model
    from django.db import OperationalError, ProgrammingError

    User = get_user_model()

    try:
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Default admin created: admin / admin123")

        # Create profile for admin safely
        from .models import UserProfile
        admin_user = User.objects.get(username='admin')
        UserProfile.objects.get_or_create(
            user=admin_user,
            role='admin',
            phone='',
            address='',
            is_approved=True  # only works if column exists
        )
    except (OperationalError, ProgrammingError) as e:
        # This usually happens if the table/column doesn't exist yet
        print("⚠ Skipping default admin profile creation, database not ready yet:", e)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)
