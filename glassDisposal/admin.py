"""
Admin configuration for the glass disposal app.

Registers the GlassDisposalEntry and RecyclingLocation models with the Django admin site.
Customizes their display to enhance usability for staff/admins managing recycling data.

Classes:
    GlassDisposalAdmin: Admin view for glass disposal entries.
    RecyclingLocationAdmin: Admin view for registered recycling bin locations.

Author:
    Charlie Shortman
"""

from django.contrib import admin
from .models import GlassDisposalEntry, RecyclingLocation


@admin.register(GlassDisposalEntry)
class GlassDisposalAdmin(admin.ModelAdmin):
    """
    Admin configuration for GlassDisposalEntry.

    Displays key details like user, location, timestamp, and coins awarded.
    Allows admin users to filter and search disposal records for easier management.

    Author:
        Charlie Shortman
    """
    list_display = ('user', 'recycling_location', 'timestamp', 'coins_awarded')  # Columns in the admin list view
    search_fields = ('user__username', 'recycling_location__name')  # Enables search by username and location name
    list_filter = ('timestamp',)  # Enables filtering by date/time


@admin.register(RecyclingLocation)
class RecyclingLocationAdmin(admin.ModelAdmin):
    """
    Admin configuration for RecyclingLocation.

    Displays location name and coordinates.
    Adds search functionality to quickly find locations.

    Author:
        Charlie Shortman
    """
    list_display = ('name', 'latitude', 'longitude')  # Columns in the admin list view
    search_fields = ('name',)  # Enables search by location name
