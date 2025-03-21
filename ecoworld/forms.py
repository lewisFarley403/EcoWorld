from django import forms
from django.utils import timezone
from .models import challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = challenge
        fields = ['name', 'description', 'worth', 'goal']  # We'll set created_by and created_on automatically

    # Optionally, override save to assign created_by and created_on
    def save(self, commit=True, created_by=None):
        instance = super().save(commit=False)
        if created_by is not None:
            instance.created_by = created_by
        # Automatically set created_on to today's date if not provided
        if not instance.created_on:
            instance.created_on = timezone.now().date()
        if commit:
            instance.save()
        return instance

