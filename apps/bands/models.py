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

# Simple internal calendar for now (swap out later for Google/ICS)
from django.db import models

class Event(models.Model):
    class Kind(models.TextChoices):
        PRACTICE = "PRACTICE", "Practice"
        GIG = "GIG", "Gig"
        OTHER = "OTHER", "Other"

    band = models.ForeignKey("Band", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.OTHER)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    # future‑proof for Google Calendar integration
    source = models.CharField(max_length=10, choices=[("MANUAL","Manual"),("GOOGLE","Google")], default="MANUAL")
    external_id = models.CharField(max_length=255, blank=True, null=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["band", "starts_at"])]

# TODO: revisit this after research on storign band photos 
class BandPhoto(models.Model):
    band = models.ForeignKey("Band", on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="band_photos/")
    caption = models.CharField(max_length=140, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]