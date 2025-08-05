from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Band(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(
        max_length=140,
        unique=True,
    )
    google_calendar_embed = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BandMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="memberships")
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
            unique_together = ("user", "band")

    def __str__(self):
        return f"{self.user.username} in {self.band.name} ({self.role})"
