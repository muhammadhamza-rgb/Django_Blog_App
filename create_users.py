import os

import django

# -----------------------
# Setup Django environment
# -----------------------
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "project.settings"
)  # replace with your project name
django.setup()

from django.contrib.auth.models import User

# -----------------------
# Create users
# -----------------------
for i in range(1, 11):
    username = f"user{i}"
    email = "muhammad.hamza@aitomation.com"
    password = "new12345"

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, email=email, password=password)
        print(f"Created user: {username}")
    else:
        print(f"User {username} already exists")
