from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserProfile, UserLibrary, UserProfileView


# Signal receiver for creating a UserProfile instance when a User instance is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Signal receiver for creating a UserLibrary instance when a UserProfile instance is created
@receiver(post_save, sender=UserProfile)
def create_user_library(sender, instance, created, **kwargs):
    if created:
        UserLibrary.objects.create(user_profile=instance)


# Signal receiver for creating a UserProfileView instance when a UserProfile instance is created
@receiver(post_save, sender=UserProfile)
def create_user_profile_view(sender, instance, created, **kwargs):
    if created:
        UserProfileView.objects.create(user_profile=instance)
