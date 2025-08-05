from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    default_band = models.ForeignKey(
        "bands.Band",
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name="default_users"
    )

    preferred_music_service = models.CharField(
        max_length=20,
        choices = [("spotify", "Spotify"), ("apple", "Apple"), ("youtube_music", "YouTube Music")],
        null=True,
        blank=True
    )
