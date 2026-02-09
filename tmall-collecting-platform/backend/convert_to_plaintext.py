#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from users.models import User

print("WARNING: Converting all user passwords to plaintext!")
print("This is only for development/testing, never for production!")

# Admin credentials
ADMIN_PASSWORDS = {
    'admin': 'admin123',
}

# Test credentials
TEST_PASSWORDS = {
    'test_user_xyz': '123456',
    'test_api_user': '123456',
    'curl_test_user': '123456',
    'final_test_user': '123456',
}

DEFAULT_PASSWORD = '123456'

count = 0
for user in User.objects.all():
    if user.username in ADMIN_PASSWORDS:
        new_password = ADMIN_PASSWORDS[user.username]
    elif user.username in TEST_PASSWORDS:
        new_password = TEST_PASSWORDS[user.username]
    else:
        new_password = DEFAULT_PASSWORD

    # Check if already plaintext (length check)
    if len(user.password) < 50:
        print(f"Skip {user.username} (already plaintext)")
        continue

    user.password = new_password
    user.save()
    count += 1
    print(f"OK {user.username}: password set to '{new_password}'")

print(f"\nDone! Updated {count} users to plaintext passwords.")
print("\nTest accounts:")
print("  Admin: admin / admin123")
print("  User: test / 123456")
