import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='rawuser')
    print(f"User: {user.username}, Password: {user.password}")
except User.DoesNotExist:
    print("User 'rawuser' not found in the configured database.")
except Exception as e:
    print(f"Error: {e}")
