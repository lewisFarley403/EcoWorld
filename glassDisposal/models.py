"""
Models for the glass disposal system.

Defines the data structure for recycling locations and disposal entries,
including user submissions with location validation and coin rewards.

Classes:
    RecyclingLocation: Represents a valid glass recycling bin with a name and coordinates.
    GlassDisposalEntry: Stores individual disposal records linked to users and locations.

Author:
    Charlie Shortman
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RecyclingLocation(models.Model):
    """
    Model representing a registered recycling location.

    Fields:
        name (CharField): Descriptive name of the recycling bin (e.g., "Streatham Bin A").
        latitude (FloatField): Geographic latitude of the bin.
        longitude (FloatField): Geographic longitude of the bin.
        created_at (DateTimeField): Timestamp when the location was added to the system.

    Author:
        Charlie Shortman
    """
    name = models.CharField(max_length=255, help_text="Recycling Bin Name")
    latitude = models.FloatField(help_text="Latitude of recycling bin")
    longitude = models.FloatField(help_text="Longitude of recycling bin")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GlassDisposalEntry(models.Model):
    """
    Model representing a single glass disposal submission made by a user.

    Fields:
        user (ForeignKey): The user who submitted the entry.
        recycling_location (ForeignKey): The location where the glass was recycled.
        image (ImageField): Photo proof uploaded by the user.
        bottle_count (PositiveIntegerField): Number of glass bottles submitted.
        timestamp (DateTimeField): The date and time of the submission.
        coins_awarded (IntegerField): Number of coins earned from the submission.

    Author:
        Charlie Shortman
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycling_location = models.ForeignKey(
        RecyclingLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='glass_disposals/',
        help_text="Photo proof of glass disposal"
    )
    bottle_count = models.PositiveIntegerField(help_text="Number of bottles disposed")
    timestamp = models.DateTimeField(default=timezone.now)
    coins_awarded = models.IntegerField(
        default=0,
        help_text="Coins earned from disposal"
    )

    def __str__(self):
        return f"{self.user.username} - {self.recycling_location} ({self.timestamp})"
