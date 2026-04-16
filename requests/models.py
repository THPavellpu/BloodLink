"""
Models for blood requests.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BloodRequest(models.Model):
    """Model for blood donation requests."""
    
    URGENCY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.CharField(max_length=5, choices=BLOOD_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=255)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Medium')
    message = models.TextField(blank=True)
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blood Request'
        verbose_name_plural = 'Blood Requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.blood_group} ({self.urgency})"
