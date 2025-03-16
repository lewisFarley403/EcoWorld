from django import forms
from .models import GlassDisposalEntry

class GlassDisposalForm(forms.ModelForm):
    """form for users to submit glass disposal entries"""
    bottle_count = forms.IntegerField(min_value=1, help_text="Enter the number of bottles you are handing in")
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = GlassDisposalEntry
        fields = ['latitude', 'longitude', 'image', 'bottle_count']
        labels = {
            'image': 'Upload Photo Proof',
            'bottle_count': 'How many bottles are you handing in?',
        }
