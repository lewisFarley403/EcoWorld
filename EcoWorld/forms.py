from django import forms
from .models import WaterBottleFill

class WaterBottleFillForm(forms.ModelForm):
    class Meta:
        model = WaterBottleFill
        fields = ['image']

