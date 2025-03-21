"""
Forms for the glass disposal app.

Defines the form used by users to submit glass recycling entries,
including bottle count, image upload, and location (latitude & longitude).

Classes:
    GlassDisposalForm: Form to handle glass disposal submissions.

Author:
    Charlie Shortman
"""

from django import forms
from .models import GlassDisposalEntry


class GlassDisposalForm(forms.ModelForm):
    """
    Form for users to submit glass disposal entries.

    Fields:
        latitude (hidden): Captures the user's current latitude from JavaScript.
        longitude (hidden): Captures the user's current longitude from JavaScript.
        image: A photo proof of the recycling action.
        bottle_count: The number of glass bottles disposed (must be at least 1).

    Meta:
        model: GlassDisposalEntry
        fields: Fields used from the model.
        labels: User-friendly labels for the form inputs.

    Author:
        Charlie Shortman
    """
    bottle_count = forms.IntegerField(
        min_value=1,
        help_text="Enter the number of bottles you are handing in"
    )
    latitude = forms.FloatField(widget=forms.HiddenInput())  # Populated via JavaScript
    longitude = forms.FloatField(widget=forms.HiddenInput())  # Populated via JavaScript

    class Meta:
        model = GlassDisposalEntry
        fields = ['latitude', 'longitude', 'image', 'bottle_count']
        labels = {
            'image': 'Upload Photo Proof',
            'bottle_count': 'How many bottles are you handing in?',
        }
