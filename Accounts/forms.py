'''
Use this module to register and authenticate users

This module provides the forms for the user to sign up and update their profile:
    - `signUpForm` : This class extends `UserCreationForm` to include an email field
    - `ProfileUpdateForm` : This class extends `ModelForm`. Allows user to change their bio and profile picture
usage:
    - SignUpForm: This class provides the form for the user to sign up. It should be imported in views.py and used in the signup view.
    
@author Ethan Sweeney (es1052@exeter.ac.uk)

'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    '''
    This class provides the form for the user to sign up. 
    It extends the UserCreationForm provided by Django to include an email field.
    Password hashing and salting is done automatically by Django when the form is 
    submitted within the userCreationForm for GDPR compliance.
    Attributes:
        email : EmailField : The email address of the user
    Methods:
        Meta : This class provides the metadata for the form.
                It specifies the model and fields to be included in the form.
    author:
        Ethan Sweeney (es1052@exeter.ac.uk)
    '''
    email = forms.EmailField(required=True)

    class Meta:
        """
        class that provides metadata for the form.
        it specifies what models from the fields to include in the form.

        Attributes:
            model : User : The User model provided by Django
            fields : list : The fields to include in the form
        """
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    """
    This class provides the form for the user to update their profile. 

    It extends the ModelForm provided by Django to include the bio and profile_picture fields.
    Attributes:
        Meta : This class provides the metadata for the form.
                It specifies the model and fields to be included in the form.
    
    author:
        -Ethan Sweeney (es1052@exeter.ac.uk
    """
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']