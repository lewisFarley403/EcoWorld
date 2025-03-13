from django import forms
from .models import ContentQuizPair

class GuidesForm(forms.ModelForm):
    class Meta:
        model = ContentQuizPair
        fields = ['title','content','quiz_questions','reward']

