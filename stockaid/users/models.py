from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """User model to contain mostly authentication-related data."""
    # Removing first and last name and using a general `name` field
    # in `UserProfile`.
    first_name = None
    last_name = None

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        # User was just created so now it needs a `UserProfile` instance.
        if created:
            UserProfile.objects.create(user=self)


class UserProfile(models.Model):
    """Model to contain all non-authentication data for a user."""

    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    title = models.CharField("Job title of User", blank=True, max_length=255)
