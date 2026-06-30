from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import CustomerProfile
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import CustomerProfile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Create profile for new users, and ensure existing users have one."""
    if created:
        CustomerProfile.objects.get_or_create(user=instance)
    else:
        # ✅ FIX: Ensure profile exists even for older users
        try:
            instance.profile.save()
        except CustomerProfile.DoesNotExist:
            CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()