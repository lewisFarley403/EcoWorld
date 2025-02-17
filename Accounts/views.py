"""
module defines views for the Accounts app:
    - `signup` : This view allows the user to sign up for an account
    - `profile` : This view allows the user to view and update their profile
author:
    - Ethan Sweeney (es1057@exeter.ac.uk) 
"""

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileUpdateForm
from .models import Profile
from .utils import createGarden, createOwnsDb
def signup(request):
    """
    This view allows the user to sign up for an account.
    It renders the signup form (when it received get request) and creates a new user when the form is submitted (it receives post request).

    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        render : HttpResponse : The HTTP response object
    Author:
        Ethan Sweeney (es1057@exeter.ac.uk)
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            print("User: ")
            print(user)
            # create garden for user
            createGarden(user)
            #creates cards owned by user set default as 0.
            createOwnsDb(user)
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'Accounts/signup.html', {'form': form})

@login_required  # Ensure that only logged-in users can access the profile
def profile(request):
    """
    This view allows the user to view and update their profile.
    It renders the profile form (when it received get request) and updates the profile when the form is submitted (it receives post request).
    it requires the user to be logged in. if the user is not logged in, it redirects to the login page.
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        render : HttpResponse : The rendered HTML page
    Author:
        - Ethan Sweeney (es1057@exeter.ac.uk)

    """
    profile = Profile.objects.get(user=request.user)

    # Handle the profile picture update
    if request.method == 'POST':
        # Get the form data
        bio = request.POST.get('bio')
        profile_picture = request.POST.get('profile_picture')

        # Update the profile
        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture  # Set the selected profile picture file name
        profile.save()

        # Redirect to the profile page after saving
        return redirect('profile')

    # If it's a GET request, show the form
    return render(request, 'Accounts/profile.html', {'profile': profile})
