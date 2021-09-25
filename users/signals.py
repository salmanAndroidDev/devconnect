from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from .models import Profile
from django.conf import settings

SUBJECT = 'WELCOME TO DEVCONNECT'
MESSAGE = """ Congratulation I have to say thank you for creating a new account
with our team. we'll definatly try so hard to make you happy with our service """


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """Receiver to create profile after user creation"""
    if created:
        profile = Profile.objects.create(user=instance,
                                         username=instance.username,
                                         email=instance.email,
                                         name=instance.first_name)
        send_mail(SUBJECT,
                  MESSAGE,
                  [settings.EMAIL_HOST_USER],
                  [profile.email],
                  fail_silently=False,
                  )


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    """Receiver to update user information based on profile information"""
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    """Receiver to delete profile after user deletion"""
    instance.user.delete()
