from django import forms
from .models import GlassDisposalEntry

class GlassDisposalForm(forms.ModelForm):
    """form for users to submit glass disposal entries"""
    bottle_count = forms.IntegerField(min_value=1, help_text="Enter the number of bottles you are handing in")

    class Meta:
        model = GlassDisposalEntry
        fields = ['location', 'image', 'bottle_count']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Enter What3Words location'}),
            'description': forms.Textarea(attrs={'placeholder': 'How many bottles did you dispose of?'}),
        }
        labels = {
            'location': 'Disposal Location (What3Words)',
            'image': 'Upload Photo Proof',
            'description': 'Description of disposal'
        }