from django import forms
from .models import ContentQuizPair


class GuidesForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

class DeleteForm(forms.Form):
    pair = forms.ModelChoiceField(queryset=ContentQuizPair.objects.all())