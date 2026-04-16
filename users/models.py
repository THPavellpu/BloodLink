"""
Custom User Model for Bloodlink system.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes blood donor specific fields.
    """
    BLOOD_CHOICES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    # Basic info
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_CHOICES, null=True, blank=True)

    # Location
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True, blank=True
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True, blank=True
    )
    location_name = models.CharField(max_length=255, null=True, blank=True)

    # Donor status
    is_available = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.blood_group})"
