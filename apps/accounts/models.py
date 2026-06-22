from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class StylePreference(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    BODY_TYPE_CHOICES = [
        ("slim", "Slim"),
        ("athletic", "Athletic"),
        ("regular", "Regular"),
        ("curvy", "Curvy"),
        ("plus", "Plus size"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True)
    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    weight_kg = models.PositiveSmallIntegerField(null=True, blank=True)
    style_preferences = models.ManyToManyField(StylePreference, blank=True, related_name="profiles")
    reference_photo = models.ImageField(upload_to="reference_photos/%Y/%m/", null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    onboarding_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile<{self.user.email}>"
