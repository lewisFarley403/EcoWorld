from django import forms
from .models import waterFountain

class WaterFountainForm(forms.ModelForm):
    class Meta:
        model = waterFountain
        fields = ['name', 'location']
