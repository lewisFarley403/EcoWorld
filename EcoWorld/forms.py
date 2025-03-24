"""
Forms for EcoWorld challenge management.

This module provides forms for creating and managing challenges in the EcoWorld game.
It includes functionality for:
    - Challenge creation with name, description, and goals
    - Automatic handling of creation timestamps
    - Challenge worth/point assignment
"""

from django import forms
from django.utils import timezone
from .models import challenge

class ChallengeForm(forms.ModelForm):
    """
    Form for creating and editing challenges.

    This form handles the creation and modification of game challenges,
    automatically managing creation timestamps and challenge creator assignment.

    Attributes:
        name (CharField): The title of the challenge
        description (TextField): Detailed description of the challenge
        worth (IntegerField): Point value for completing the challenge
        goal (IntegerField): Target number for challenge completion
    """
    class Meta:
        """
        Metadata for the ChallengeForm.

        Specifies the model and fields to be included in the form.

        Attributes:
            model: Challenge model for game challenges
            fields: List of editable challenge fields
        """
        model = challenge
        fields = ['name', 
                  'description', 
                  'worth', 
                  'goal']  # We'll set created_by and created_on automatically

    # Optionally, override save to assign created_by and created_on
    def save(self, commit=True, created_by=None):
        """
        Save the challenge form with automatic field population.

        Extends the standard form save method to automatically handle
        creation timestamp and creator assignment.

        Args:
            commit (bool): Whether to commit the save to the database
            created_by (User): The user creating the challenge

        Returns:
            Challenge: The saved challenge instance
        """
        instance = super().save(commit=False)
        if created_by is not None:
            instance.created_by = created_by
        # Automatically set created_on to today's date if not provided
        if not instance.created_on:
            instance.created_on = timezone.now().date()
        if commit:
            instance.save()
        return instance
