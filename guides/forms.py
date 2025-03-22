from django import forms

from .models import ContentQuizPair


class GuidesForm(forms.Form):
    """
    This class provides the form for the gamekeeper to add a guide
    Attributes:
        title : this attribute is the title of the guide
        content : this attribute is for the content section of the guide (supports Markdown)
    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
    title = forms.CharField(
        label="Title",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    content = forms.CharField(
        label="Content (Markdown supported)",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 
                                    'placeholder': 'This field supports Markdown formatting. Examples:\n\n# Heading 1\n## Heading 2\n\n**Bold text** or __bold text__\n*Italic text* or _italic text_\n\n- Bullet point\n1. Numbered list\n\n[Link text](https://example.com)\n\n```\nCode block\n```'}))

class DeleteForm(forms.Form):
    """
    This class provides the form for the gamekeeper to remove a guide
    Attributes:
        pair : the reference to the pair that the gamekeeper wants to
            delete
    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
    pair = forms.ModelChoiceField(queryset=ContentQuizPair.objects.all())