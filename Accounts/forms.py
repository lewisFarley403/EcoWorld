from django import forms
from .models import User
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'date_of_birth']
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # ✅ Hash the password before saving

        if commit:
            user.save()  
        return user
