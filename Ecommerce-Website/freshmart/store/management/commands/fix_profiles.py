from django.contrib.auth.models import User
from store.models import CustomerProfile
for user in User.objects.all():
    CustomerProfile.objects.get_or_create(user=user)
    print(f"Fixed: {user.username}")